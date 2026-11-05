"""Parse a proposal (markdown PRD / opportunity brief) into sections and metric bullets."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Bullet:
    text: str
    kind: str  # success | guardrail


@dataclass
class PRD:
    raw: str
    title: str
    sections: dict = field(default_factory=dict)  # lowercased heading -> text
    bullets: list = field(default_factory=list)

    @property
    def narrative(self) -> str:
        """Everything except metric sections and the experiment plan (used for category and claim detection)."""
        parts = [self.title]
        for h, t in self.sections.items():
            if not _is_metric_heading(h) and "experiment" not in h:
                parts.append(t)
        return "\n".join(parts)

    @property
    def experiment_text(self) -> str:
        return "\n".join(t for h, t in self.sections.items() if "experiment" in h or "test plan" in h)

    @property
    def metric_text(self) -> str:
        return "\n".join(b.text for b in self.bullets)


def _is_metric_heading(h: str) -> bool:
    return bool(re.search(r"metric|kpi|guardrail|success", h))


def parse_prd(raw: str) -> PRD:
    title_m = re.search(r"^#\s+(.+)$", raw, flags=re.M)
    title = title_m.group(1).strip() if title_m else ""
    sections: dict = {}
    for part in re.split(r"^##\s+", raw, flags=re.M)[1:]:
        head, _, body = part.partition("\n")
        sections[head.strip().lower()] = body.strip()
    bullets = []
    for h, t in sections.items():
        if not _is_metric_heading(h):
            continue
        kind = "guardrail" if "guardrail" in h else "success"
        for line in t.splitlines():
            m = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.+)$", line)
            if m:
                bullets.append(Bullet(m.group(1).strip(), kind))
    return PRD(raw=raw, title=title, sections=sections, bullets=bullets)


def contains_term(text: str, term: str) -> bool:
    """Word-boundary, case-insensitive match; allows a trailing plural s/es."""
    return re.search(r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?:es|s)?(?![a-z0-9])", text.lower()) is not None
