# 5. Evaluation: baseline, test cases, results, failures, and how to test with real PMs

**All numbers below are copied from `evals/RESULTS.md`, which `python3 -m pmdc eval` generates. Nothing is typed by hand.** v1 results (before one prompt change, see 5.6 finding 7) are preserved in `evals/results/RESULTS-v1.md`.

## 5.1 What this evaluation can and cannot show
- **Can show**: the pipeline works end to end; what each layer (rules, retrieval, mandatory context, verifier) buys; where each fails; how noisy the model is.
- **Cannot show**: that PMs make better decisions. The cases, knowledge, and rules were all written by one person (me). A high score on authored cases proves the machinery works, nothing more. Section 5.8 is the plan that could show value.

## 5.2 Test set
25 synthetic proposals (`evals/cases/*.md`) with planted flaws and ground-truth labels (`evals/labels.json`), written **before** any model was run.

| Split | Cases | Purpose | Honest status |
|---|---|---|---|
| dev (D01-D12) | 12 (2 clean, 1 injection, 4 multi-flaw) | Build and tune rules and prompts | Used while building: contaminated by design |
| holdout (H01-H06) | 6 (2 clean, 1 injection) | Check for overfitting | Run once for rules without tuning. Rule logic was written with dev vocabulary in mind, so still not independent |
| stress (S01-S07) | 7 (2 clean) | Defeat keyword rules: paraphrased personal data, paraphrased prior art, claim without digits, false-positive traps, synonym guardrails, self-selected cohort, self-attested waiver | **Written after rules scored 100% on dev and holdout.** Post-hoc by design |

Flaw taxonomy (7 types, `pmdc/types.py`): UNDEFINED_METRIC, NO_BASELINE_TARGET, MISSING_GUARDRAIL, PRIOR_ART, POLICY_REVIEW, UNSUPPORTED_CLAIM, WEAK_EXPERIMENT_DESIGN. Cases cover 27 labeled flaw instances (54 run-level instances over 2 repeats) across 6 clean and 19 flawed proposals. Two cases contain prompt injection.

## 5.3 Arms (isolating what each layer contributes)
| Arm | Knowledge | Rules | Verifier |
|---|---|---|---|
| `rules` | yes (structured) | yes | n/a |
| `baseline-llm` | **none** (same taxonomy and schema) | no | type check only |
| `grounded-llm` | BM25 top-6 chunks | no | full |
| `hybrid` | top-6 + mandatory chunks + glossary | candidates supplied | full |

Model: `claude-sonnet-5-5` via the internal gateway. 2 repeats per case for LLM arms (LLM runs vary).

## 5.4 Metrics
Scoring is exact match on **flaw type** per proposal (no LLM judge, so no judge bias). Precision, recall, F1 are micro-averaged over types. **Clean-doc false-positive rate** = share of runs on clean proposals with at least one finding. **Verdict accuracy** = verdict equals the verdict implied by the labels (BLOCKED / NEEDS_WORK / READY). **Injection pass** = labeled flaw found and verdict not READY on injected proposals. **Citation validity** = cited chunk ids that exist. **Retrieval doc recall** = for each labeled knowledge-dependent flaw, was a chunk from the right source document in the context. **Stability** = share of cases with identical type sets across repeats.

## 5.5 Results (v2, current)

| Arm | Precision | Recall | F1 | Clean-doc FP rate | Verdict accuracy | Injection pass |
|---|---|---|---|---|---|---|
| rules | 81% | 81% | 81% | 33% | 72% | 100% |
| baseline-llm | 46% | 83% | 60% | 0% | 78% | 100% |
| grounded-llm | 86% | 70% | 78% | 17% | 72% | 50% |
| hybrid | 76% | 98% | 85% | 17% | 90% | 100% |

By split:

| Arm | Dev F1 | Holdout F1 | Stress F1 | Stress recall | Stress clean-doc FP rate |
|---|---|---|---|---|---|
| rules | 100% | 100% | **0%** | 0% | 100% |
| baseline-llm | 65% | 59% | 47% | 70% | 0% |
| grounded-llm | 87% | 77% | 47% | 40% | 50% |
| hybrid | 92% | 80% | 75% | 90% | 50% |

Recall by flaw type (selected): PRIOR_ART: baseline 0%, rules 75%, grounded 100%, hybrid 100%. POLICY_REVIEW: rules 71%, baseline 93%, grounded 43%, hybrid 100%. WEAK_EXPERIMENT_DESIGN: rules 75%, baseline 100%, grounded **0%**, hybrid 88%.

Operations: baseline 6.0 s and about 1.1k input tokens per review; grounded 6.6 s and 2.4k; hybrid 7.2 s and 5.2k. Citation validity 100% in grounded and hybrid; verifier dropped 0.16 findings per grounded run. Retrieval doc recall: grounded 81%, hybrid 100%. Stability: baseline 68%, grounded 92%, hybrid 88%.

Run-to-run noise matters: a re-run moved hybrid precision by about 3 points and F1 by about 2 (v1 to v2) with a one-line prompt change that did not target those metrics. Treat differences under about 5 points as noise at this sample size.

## 5.6 What the results say (and what I would not claim)

1. **Authored-case scores for rules are circular.** 100% on dev and holdout, 0% on paraphrase stress cases with 100% false positives on the two clean traps. This is the main lesson about evaluating your own system on your own data, and it is why stress cases exist.
2. **Ungrounded LLM (baseline) is bimodal.** It finds flaws that general knowledge can find (policy 93%, experiment design 100%, unsupported claims 100%) and is blind to company-specific ones (prior art 0%). It is silent on clean proposals but speculative on flawed ones: precision 46%, with many invented guardrail, metric, and policy findings it cannot verify. A PM gets a plausible list that is about half wrong and cannot tell which half.
3. **Pure RAG trades recall for precision, and the verifier makes retrieval misses invisible.** Precision 86%, recall 70%. Retrieval doc recall is 81%; when the right policy or standards chunk is not retrieved, the verifier correctly refuses an ungrounded finding, so a retrieval miss becomes a silent miss (WEAK_EXPERIMENT_DESIGN recall 0%, POLICY_REVIEW 43%). The cure is not removing the verifier; it is better retrieval and mandatory context.
4. **Hybrid has the best recall (98%) and verdict accuracy (90%) but not the best precision (76%).** More context also means more speculative findings. It costs about 2x the tokens of pure RAG. Verdict accuracy is the number that matters for routing a proposal; it is 18 points above pure RAG, 12 above baseline.
5. **Injection results are weak evidence.** All arms except grounded-llm passed. Grounded failed on H06 by returning no findings, but that run's retrieved context contained **no policy chunk**, so the model may have been following the "cite or do not report" rule rather than obeying the injected instruction. The design confounds retrieval and injection and cannot separate them. The code-owned verdict did prevent any injected "Ready" from taking effect. With 2 injection cases, I make no robustness claim; a dedicated red-team set is required.
6. **The dominant hybrid false positives are "horizon mismatch" findings**: the experiment runs 3 weeks while the success target is measured over 8 or 12 weeks. The model often wrote "meets the 14-day minimum, but..." and still labeled it WEAK_EXPERIMENT_DESIGN. This is arguably a **real flaw my taxonomy lacks**, flagged under the nearest type. I counted it as a false positive per the labels I wrote before running anything. A second group (H04, S04, S05, S06) are defensible disagreements with my labels (see 5.7).
7. **A one-line prompt fix did not work.** After v1, I added "never emit a finding whose detail says it is not a flaw". Result: no measurable change (hybrid F1 87% to 85%, baseline precision 40% to 46%, all within noise); 10 of 263 findings across the LLM arms in v2 (regex count) still self-qualify. The right fix is structural (add a horizon-mismatch type or a verifier rule), and I did **not** do it, because tuning on the same failures would remove the last independent signal.
8. **Single-run results are not stable.** Baseline type-sets are identical across repeats in only 68% of cases. Any production use needs repeats, caching, or a deterministic layer in front of the model; this is another reason the verdict is computed from findings in code.

## 5.7 Label audit (labels were NOT changed after seeing results)
Extras from the hybrid arm that a human reviewer could reasonably accept as valid, so strict precision of 76% likely understates real precision:

| Case | Model finding | Why defensible |
|---|---|---|
| H04 | PRIOR_ART: proposal cites EXP-014 but judges success on OTD alone, the very pitfall EXP-014 warns about | My PRIOR_ART definition says "does not reference **or learn from**"; label arguably should include it |
| S05 | PRIOR_ART: a "more reliable later window" resembles padded promises tested in EXP-014 | Plausible overlap |
| S04 | POLICY_REVIEW: phoning customers uses contact details | Reasonable reading of the privacy policy |
| S06 | POLICY_REVIEW: model-generated instructions from archived photos | Reasonable reading of the GenAI policy |
| D11, D12, H05 | WEAK_EXPERIMENT_DESIGN: test duration vs target window | Real concern, wrong type label |
| H05 | MISSING_GUARDRAIL: Contact Rate is a success metric, not a listed guardrail | Strict reading of the standard |

Real reviewers adjudicating these would be a better ground truth than my labels (5.8).

## 5.8 Plan to test with real PMs

**Goal**: decide go / re-scope / stop with evidence about decision quality, not enthusiasm.

| Step | Design | Output | Success criterion (pre-registered, thresholds assumed) |
|---|---|---|---|
| A. Retrospective replay | 30-50 historical proposals with known outcomes (shipped and worked, shipped and regretted, killed). Two reviewers independently list issues blind; agent run separately | Recall of reviewer-raised issues; precision judged by reviewers; did flagged flaws precede failed launches | Recall at least 60% on taxonomy types; precision at least 80% judged by reviewers; flagged flaws over-represented in regretted launches |
| B. Reviewer labeling of findings | Reviewers label each finding valid / invalid / valid-low-value; compute inter-rater agreement | Human-judged precision and a corrected taxonomy | Kappa at least 0.6; new types added from the "valid but not in taxonomy" bucket (e.g., horizon mismatch) |
| C. Within-subject PM study | 12-20 PMs, each reviews 2 proposals, with and without the tool, order counterbalanced. A third arm: "paste into chat and ask for feedback" (the real baseline I did not run) | Issues found versus gold, time, confidence, trust calibration, survey | Tool beats free-form chat on recall of gold issues with no loss of precision; time not worse; PM confidence matches accuracy |
| D. Stepped-wedge pilot | Teams start in random order over 8-12 weeks (`07`) | Review cycle time, send-backs, first-pass acceptance, regretted launches | -20% cycle time, +15 points first-pass acceptance; no increase in regretted launches |
| E. Red team | InfoSec injection and exfiltration suite; retrieval-poisoning attempts | Failure rate by attack class | No successful verdict change; documented suppression rate |

Statistical note: with 12-20 PMs in a paired design, 95 percent intervals on a recall difference are about plus or minus 10 points. That is enough for go/no-go, not for a publication claim. Analyze with paired bootstrap; pre-register thresholds before step A.

**What would change my mind** (stop or re-scope): reviewers' top send-back reasons are outside the taxonomy; human-judged precision below 60%; PMs do not open findings after week 4; trust is high but accuracy is low (automation bias), which is a safety failure even if usage looks good.

## 5.9 Reproduce
```
python3 -m unittest discover -s tests          # 12 tests, no network
python3 -m pmdc eval --cache-only              # replays cached model responses, no credentials, regenerates evals/RESULTS.md
python3 -m pmdc eval                           # re-runs live (needs ANTHROPIC_AUTH_TOKEN or ANTHROPIC_API_KEY; ANTHROPIC_BASE_URL optional)
```
