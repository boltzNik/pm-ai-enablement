"""Shared types: flaw taxonomy, severity policy, findings, and the code-computed verdict."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

TAXONOMY = {
    "UNDEFINED_METRIC": "A success or guardrail metric is not a canonical, defined metric in the company metrics glossary (vague, ambiguous, or deprecated name).",
    "NO_BASELINE_TARGET": "A success metric lacks a baseline, a numeric target, or a timeframe.",
    "MISSING_GUARDRAIL": "The proposal changes behavior in an area that requires specific guardrail metrics, and one or more required guardrails are absent.",
    "PRIOR_ART": "The proposal substantially repeats a previous experiment or decision and does not reference or learn from it.",
    "POLICY_REVIEW": "The proposal touches a regulated or policy-controlled area (pay, personal data, age-restricted items, generative AI) and does not record the required review.",
    "UNSUPPORTED_CLAIM": "A quantitative claim (percentage, dollar amount, multiplier) is stated as fact without a source.",
    "WEAK_EXPERIMENT_DESIGN": "The validation plan is missing or violates experimentation standards (randomization unit leaks between arms, duration under 14 days, no MDE or power, no plan).",
}
# Code-owned severity: the LLM never decides how serious a finding is or what the verdict is.
SEVERITY = {
    "POLICY_REVIEW": "high", "MISSING_GUARDRAIL": "high", "WEAK_EXPERIMENT_DESIGN": "high",
    "PRIOR_ART": "medium", "UNDEFINED_METRIC": "medium", "NO_BASELINE_TARGET": "medium", "UNSUPPORTED_CLAIM": "medium",
}
# Which knowledge doc must ground each type (used for citation gating and retrieval recall).
GROUNDING_DOC = {
    "UNDEFINED_METRIC": "metrics-glossary", "MISSING_GUARDRAIL": "guardrail-standards",
    "PRIOR_ART": "experiment-registry", "POLICY_REVIEW": "policy-compliance",
    "WEAK_EXPERIMENT_DESIGN": "experimentation-standards",
}


@dataclass
class Finding:
    type: str
    title: str
    detail: str
    recommendation: str = ""
    evidence_quote: str = ""
    citations: list = field(default_factory=list)
    source: str = "rules"

    @property
    def severity(self) -> str:
        return SEVERITY.get(self.type, "low")

    def to_dict(self) -> dict:
        d = asdict(self)
        d["severity"] = self.severity
        return d


def verdict_for(types: set[str]) -> str:
    if "POLICY_REVIEW" in types:
        return "BLOCKED"
    return "NEEDS_WORK" if types else "READY"
