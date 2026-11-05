"""Deterministic checks. Each check is a pure function (PRD, KB) -> list[Finding].

These are the "tools" the agent can trust: reproducible, auditable, zero hallucination risk.
They are also deliberately shallow (keyword and regex based) - see docs/05-evaluation.md for where they fail.
"""
from __future__ import annotations

import re
from datetime import date

from .kb import KB, Chunk
from .prd import PRD, contains_term
from .types import Finding

SOURCE_MARKERS = re.compile(
    r"(source:|according to|dashboard|query|report|study|analysis|audit|EXP-\d+|\[\d+\]|https?://|time study)", re.I)
NUMERIC_CLAIM = re.compile(r"\$\s?\d[\d,.]*\s?(?:k|m|b|million|billion)?\b|\d+(?:\.\d+)?\s?%|\b\d+(?:\.\d+)?x\b", re.I)


def _glossary(kb: KB) -> list[Chunk]:
    return [c for c in kb.of_doc("metrics-glossary") if "name" in c.attrs and "deprecated_terms" not in c.attrs]


def _metric_terms(c: Chunk) -> list[str]:
    return [c.attrs["name"], *c.attrs.get("aliases", [])]


def _mentions_metric(text: str, c: Chunk) -> bool:
    return any(contains_term(text, t) for t in _metric_terms(c))


def triggered_categories(prd: PRD, kb: KB) -> list[Chunk]:
    return [c for c in kb.of_doc("guardrail-standards")
            if any(contains_term(prd.narrative, t) for t in c.attrs.get("trigger_terms", []))]


def check_undefined_metrics(prd: PRD, kb: KB) -> list[Finding]:
    glossary = _glossary(kb)
    deprecated = next((c for c in kb.of_doc("metrics-glossary") if "deprecated_terms" in c.attrs), None)
    out = []
    for b in prd.bullets:
        label = re.split(r":", b.text, maxsplit=1)[0]
        if any(_mentions_metric(label, c) for c in glossary):
            continue
        dep_hit = deprecated and next((t for t in deprecated.attrs["deprecated_terms"] if contains_term(label, t)), None)
        cites = [deprecated.id] if dep_hit and deprecated else []
        out.append(Finding(
            "UNDEFINED_METRIC", f"Metric not in glossary: '{label.strip()}'",
            f"'{label.strip()}' does not match any canonical LMD metric or alias." + (f" '{dep_hit}' is a deprecated or ambiguous term." if dep_hit else ""),
            "Replace with a canonical metric (see glossary guidance) or propose adding a new definition with an owner.",
            evidence_quote=b.text[:160], citations=cites))
    return out


def check_baseline_target(prd: PRD, kb: KB) -> list[Finding]:
    out = []
    for b in prd.bullets:
        if b.kind != "success":
            continue
        time_re = re.compile(r"\b\d+\s*(?:day|week|month)s?\b|\bq[1-4]\b|\bend of\b", re.I)
        has_time = bool(time_re.search(b.text))
        nums = re.findall(r"\d+(?:\.\d+)?", time_re.sub(" ", b.text))
        has_base_target = len(nums) >= 2 or ("baseline" in b.text.lower() and len(nums) >= 1)
        if not (has_time and has_base_target):
            missing = [x for x, ok in (("baseline and numeric target", has_base_target), ("timeframe", has_time)) if not ok]
            out.append(Finding(
                "NO_BASELINE_TARGET", f"Success metric lacks {' and '.join(missing)}",
                f"'{b.text[:100]}' cannot be evaluated later without a baseline, numeric target and timeframe.",
                "State baseline, target and timeframe, e.g. 'from X to Y within N weeks'.", evidence_quote=b.text[:160]))
    return out


def check_guardrails(prd: PRD, kb: KB) -> list[Finding]:
    glossary = {c.attrs["name"]: c for c in _glossary(kb)}
    text = prd.metric_text or prd.raw
    out = []
    for cat in triggered_categories(prd, kb):
        missing = [m for m in cat.attrs.get("required_guardrails", [])
                   if m in glossary and not _mentions_metric(text, glossary[m])]
        if missing:
            out.append(Finding(
                "MISSING_GUARDRAIL", f"Missing guardrails for '{cat.attrs.get('category', cat.heading)}'",
                f"This change touches {cat.attrs.get('category', cat.heading)}. Required guardrails not found: {', '.join(missing)}.",
                "Add each missing metric with a stop threshold.", citations=[cat.id]))
    return out


def check_prior_art(prd: PRD, kb: KB) -> list[Finding]:
    out = []
    for c in kb.of_doc("experiment-registry"):
        hits = [k for k in c.attrs.get("keywords", []) if contains_term(prd.narrative, k)]
        exp_id = c.heading.split()[0]
        if len(hits) >= 2 and exp_id not in prd.raw:
            out.append(Finding(
                "PRIOR_ART", f"Overlaps {exp_id} which is not referenced",
                f"Matched terms: {', '.join(hits)}. Registry says: {c.text.splitlines()[0] if c.text else ''}",
                f"Read {exp_id}, state what is different this time, and reuse its learning.", citations=[c.id]))
    return out


def check_policy(prd: PRD, kb: KB) -> list[Finding]:
    out = []
    low = prd.raw.lower()
    for c in kb.of_doc("policy-compliance"):
        hits = [t for t in c.attrs.get("trigger_terms", []) if contains_term(prd.narrative, t)]
        if hits and not any(m in low for m in c.attrs.get("review_markers", [])):
            out.append(Finding(
                "POLICY_REVIEW", f"{c.attrs.get('required_review', 'Review')} not recorded",
                f"Triggered by: {', '.join(hits)}. No evidence of {c.attrs.get('required_review', 'review')} in the document.",
                f"Obtain {c.attrs.get('required_review', 'the review')} and record the ticket reference before build.", citations=[c.id]))
    return out


def check_unsupported_claims(prd: PRD, kb: KB) -> list[Finding]:
    out = []
    for sent in re.split(r"(?<=[.!?])\s+|\n", prd.narrative):
        if NUMERIC_CLAIM.search(sent) and not SOURCE_MARKERS.search(sent):
            out.append(Finding(
                "UNSUPPORTED_CLAIM", "Quantitative claim without a source", f"'{sent.strip()[:140]}' has no source.",
                "Cite the dashboard, query, study or experiment, or label it an assumption.", evidence_quote=sent.strip()[:160]))
    return out


def check_experiment(prd: PRD, kb: KB) -> list[Finding]:
    std = {c.heading: c for c in kb.of_doc("experimentation-standards")}
    interference = std.get("Marketplace Interference")
    text = prd.experiment_text
    if not re.search(r"randomi[sz]|a/b|switchback|pilot|holdout|geo|experiment", text, re.I):
        return [Finding("WEAK_EXPERIMENT_DESIGN", "No validation plan", "No experiment or staged rollout with a control was found.",
                        "Add a design with randomization unit, duration, MDE and stopping rule.",
                        citations=[std["Pre-Registration"].id] if "Pre-Registration" in std else [])]
    issues, cites = [], []
    days = [int(n) * (7 if u.lower().startswith("week") else 1) for n, u in re.findall(r"(\d+)\s*[- ]?\s*(day|week)s?", text, re.I)]
    if not days or max(days) < 14:
        issues.append("duration under 14 days or not stated")
        cites.append("experimentation-standards#duration-and-seasonality")
    if not re.search(r"\b(mde|minimum detectable|power|sample size)\b", text, re.I):
        issues.append("no MDE, power or sample size")
        cites.append("experimentation-standards#pre-registration")
    if interference:
        applies = set(interference.attrs.get("applies_to_categories", []))
        cats = {c.attrs.get("category") for c in triggered_categories(prd, kb)}
        individual = re.search(r"randomi[sz]ed\s+(?:at\s+the\s+|by\s+|at\s+|per\s+)?(?:customer|user|driver|order)\b", text, re.I)
        clustered = re.search(r"switchback|geo|market|cluster|zone|store", text, re.I)
        if applies & cats and individual and not clustered:
            issues.append("individual-level randomization for a change that interferes across the shared supply pool")
            cites.append(interference.id)
    if not issues:
        return []
    return [Finding("WEAK_EXPERIMENT_DESIGN", "Experiment design gaps", "; ".join(issues).capitalize() + ".",
                    "Use a switchback, geo or market design, at least 14 days, and pre-register MDE and stopping rule.", citations=cites)]


ALL_CHECKS = [check_undefined_metrics, check_baseline_target, check_guardrails, check_prior_art,
              check_policy, check_unsupported_claims, check_experiment]


def run_checks(prd: PRD, kb: KB) -> list[Finding]:
    return [f for chk in ALL_CHECKS for f in chk(prd, kb)]


def stale_sources(kb: KB, cited: set[str], today: date | None = None, max_days: int = 120) -> list[str]:
    today = today or date.today()
    out = []
    for cid in sorted(cited):
        c = kb.by_id.get(cid)
        if not c:
            continue
        try:
            age = (today - date.fromisoformat(c.meta.get("last_reviewed", ""))).days
        except ValueError:
            continue
        if age > max_days:
            out.append(f"{cid} last reviewed {age} days ago (owner: {c.meta.get('owner', '?')})")
    return out
