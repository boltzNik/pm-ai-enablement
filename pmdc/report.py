from __future__ import annotations

from .agent import Review
from .checks import stale_sources
from .kb import KB

VERDICT_TEXT = {
    "READY": "READY for human review. No taxonomy flaws found.",
    "NEEDS_WORK": "NEEDS WORK before human review.",
    "BLOCKED": "BLOCKED: a required policy review is not recorded.",
}


def to_markdown(r: Review, kb: KB, title: str = "", stale_days: int = 120) -> str:
    out = [f"# Decision Readiness Review{': ' + title if title else ''}", "",
           f"**Verdict: {VERDICT_TEXT[r.verdict]}**  (mode: `{r.mode}`)", ""]
    if not r.findings:
        out.append("No findings.")
    cited: set[str] = set()
    for sev in ("high", "medium", "low"):
        group = [f for f in r.findings if f.severity == sev]
        if not group:
            continue
        out += [f"## {sev.capitalize()} severity", ""]
        for f in group:
            out.append(f"- **{f.type}: {f.title}**")
            out.append(f"  - Why: {f.detail}")
            if f.evidence_quote:
                out.append("  - Evidence: \"" + " ".join(f.evidence_quote.split()) + "\"")
            if f.recommendation:
                out.append(f"  - Fix: {f.recommendation}")
            if f.citations:
                out.append("  - Sources: " + ", ".join(f"`{c}`" for c in f.citations))
                cited.update(f.citations)
        out.append("")
    stale = stale_sources(kb, cited, max_days=stale_days)
    if stale:
        out += ["## Source freshness warnings", ""] + [f"- {s}" for s in stale] + [""]
    dropped = r.meta.get("dropped") or []
    if dropped:
        out += [f"_Verifier dropped {len(dropped)} model finding(s): " + ", ".join(sorted({d['reason'] for d in dropped})) + "._", ""]
    out += ["---", "Advisory pre-review only. It is not an approval and does not replace Legal, Privacy, Compliance, or Data Science review. "
            "All sources are synthetic in this prototype."]
    return "\n".join(out)
