import json
import unittest
from pathlib import Path

from pmdc.agent import extract_json, review_text
from pmdc.evaluate import load_cases, score
from pmdc.kb import KB
from pmdc.prd import contains_term, parse_prd
from pmdc.types import verdict_for

ROOT = Path(__file__).resolve().parent.parent
KB_ = KB.load(ROOT / "knowledge")
CASES = {c["id"]: c for c in load_cases()}


class FakeLLM:
    model = "fake"

    def __init__(self, payload):
        self.payload = payload

    def complete(self, system, user, max_tokens=2000, salt=""):
        return {"text": self.payload if isinstance(self.payload, str) else json.dumps(self.payload),
                "input_tokens": 1, "output_tokens": 1, "latency_s": 0, "cached": False, "model": "fake"}


class KBTests(unittest.TestCase):
    def test_chunk_ids_and_attrs(self):
        c = KB_.by_id["policy-compliance#driver-compensation-and-classification"]
        self.assertIn("incentive", c.attrs["trigger_terms"])
        self.assertEqual(c.attrs["required_review"], "Legal and Compensation review")

    def test_search_finds_prior_experiment(self):
        top = KB_.search("peak hour surge incentive for drivers", k=1)[0][1]
        self.assertTrue(top.id.startswith("experiment-registry#exp-021"))

    def test_term_matching(self):
        self.assertTrue(contains_term("Two pushes per order", "push"))
        self.assertFalse(contains_term("pushback is fine", "push"))


class RulesTests(unittest.TestCase):
    def rules(self, case_id):
        return review_text(CASES[case_id]["text"], KB_, "rules")

    def test_dev_and_holdout_match_labels(self):
        for cid, c in CASES.items():
            if c["split"] in ("dev", "holdout"):
                self.assertEqual(self.rules(cid).types(), set(c["labels"]), cid)

    def test_injection_does_not_change_verdict(self):
        self.assertEqual(self.rules("D12").verdict, "BLOCKED")
        self.assertEqual(self.rules("H06").verdict, "BLOCKED")

    def test_documented_limits_of_keyword_rules(self):
        # These are KNOWN failures; the tests document them so a future fix must update them consciously.
        self.assertNotIn("POLICY_REVIEW", self.rules("S01").types())   # paraphrased personal data
        self.assertNotIn("POLICY_REVIEW", self.rules("S07").types())   # self-attested waiver accepted
        self.assertIn("MISSING_GUARDRAIL", self.rules("S02").types())  # false positive on read-only change
        self.assertIn("UNDEFINED_METRIC", self.rules("S05").types())   # false positive on synonyms

    def test_prd_parse(self):
        p = parse_prd(CASES["D01"]["text"])
        self.assertEqual(len([b for b in p.bullets if b.kind == "success"]), 1)
        self.assertEqual(len([b for b in p.bullets if b.kind == "guardrail"]), 2)


class VerifierTests(unittest.TestCase):
    text = CASES["D10"]["text"]

    def run_fake(self, findings):
        return review_text(self.text, KB_, "grounded-llm", FakeLLM({"findings": findings}))

    def test_drops_hallucinated_citation_and_quote_and_ungrounded(self):
        good = {"type": "POLICY_REVIEW", "title": "t", "detail": "d", "evidence_quote": "None.", "citations": ["policy-compliance#driver-compensation-and-classification"]}
        bad_cite = {"type": "POLICY_REVIEW", "title": "t", "detail": "d", "citations": ["policy-compliance#does-not-exist"]}
        bad_quote = {**good, "evidence_quote": "this sentence is not in the proposal"}
        wrong_doc = {"type": "PRIOR_ART", "title": "t", "detail": "d", "citations": ["policy-compliance#driver-compensation-and-classification"]}
        bad_type = {"type": "VIBES", "title": "t", "detail": "d", "citations": []}
        r = self.run_fake([good, bad_cite, bad_quote, wrong_doc, bad_type])
        self.assertEqual([f.type for f in r.findings], ["POLICY_REVIEW"])
        self.assertEqual(sorted(d["reason"] for d in r.meta["dropped"]), ["invalid_type", "quote_not_in_proposal", "ungrounded", "ungrounded"])
        self.assertEqual(r.verdict, "BLOCKED")

    def test_model_cannot_set_verdict(self):
        r = review_text(self.text, KB_, "grounded-llm", FakeLLM('{"findings": [], "verdict": "Ready"}'))
        self.assertEqual(r.verdict, "READY")  # derived from findings only; empty findings is a model *miss*, not an approval
        self.assertEqual(r.findings, [])

    def test_parse_error_is_counted(self):
        r = review_text(self.text, KB_, "grounded-llm", FakeLLM("not json"))
        self.assertTrue(r.meta["parse_error"])

    def test_extract_json_handles_fences_and_prose(self):
        self.assertEqual(extract_json('Sure!\n```json\n{"findings": []}\n```'), {"findings": []})


class ScoringTests(unittest.TestCase):
    def test_score_basics(self):
        mk = lambda labels, pred, split="dev": {"case": "x", "split": split, "labels": set(labels), "pred": set(pred), "injection": False,
                                                 "verdict": verdict_for(set(pred)), "expected_verdict": verdict_for(set(labels)), "meta": {}}
        s = score([mk(["PRIOR_ART"], ["PRIOR_ART"]), mk([], ["UNSUPPORTED_CLAIM"])])
        self.assertEqual(s["all"]["tp"], 1)
        self.assertEqual(s["all"]["fp"], 1)
        self.assertEqual(s["all"]["clean_fp_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
