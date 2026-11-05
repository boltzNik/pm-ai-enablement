"""Knowledge base: markdown files -> chunks with provenance metadata + BM25 retrieval. Stdlib only."""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

LIST_KEYS = {
    "aliases", "trigger_terms", "required_guardrails", "review_markers", "keywords",
    "applies_to_categories", "acceptable_designs", "deprecated_terms",
}
ATTR_KEYS = LIST_KEYS | {"name", "category", "required_review", "status", "min_days"}
_TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def slug(text: str) -> str:
    return "-".join(tokenize(text))


@dataclass
class Chunk:
    id: str
    doc_id: str
    doc_type: str
    heading: str
    text: str
    attrs: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

    def label(self) -> str:
        return f"[{self.id}] ({self.doc_type}, owner: {self.meta.get('owner', '?')}, reviewed: {self.meta.get('last_reviewed', '?')})"


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    meta = {}
    for line in raw[3:end].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, raw[end + 4:].lstrip("\n")


def _parse_section(body: str) -> tuple[dict, str]:
    attrs, rest = {}, []
    for line in body.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.+)$", line.strip())
        if m and m.group(1) in ATTR_KEYS:
            k, v = m.group(1), m.group(2).strip()
            attrs[k] = [x.strip() for x in v.split(";") if x.strip()] if k in LIST_KEYS else v
        else:
            rest.append(line)
    return attrs, "\n".join(rest).strip()


def load_chunks(path: str | Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for f in sorted(Path(path).glob("*.md")):
        meta, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        doc_id = meta.get("id", f.stem)
        parts = re.split(r"^## ", body, flags=re.M)
        for part in parts[1:]:
            heading, _, sect = part.partition("\n")
            attrs, text = _parse_section(sect)
            chunks.append(Chunk(
                id=f"{doc_id}#{slug(heading)}", doc_id=doc_id, doc_type=meta.get("type", "doc"),
                heading=heading.strip(), text=text, attrs=attrs, meta=meta,
            ))
    return chunks


class KB:
    """Small in-memory index. Swap for an enterprise search/MCP connector in production."""

    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.by_id = {c.id: c for c in chunks}
        self.k1, self.b = k1, b
        self._docs = [tokenize(c.heading + " " + c.heading + " " + c.text + " " + " ".join(
            x for v in c.attrs.values() for x in (v if isinstance(v, list) else [v]))) for c in chunks]
        self._avg = sum(len(d) for d in self._docs) / max(len(self._docs), 1)
        df = Counter(t for d in self._docs for t in set(d))
        n = len(self._docs)
        self._idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    @classmethod
    def load(cls, path: str | Path) -> "KB":
        return cls(load_chunks(path))

    def search(self, query: str, k: int = 6, doc_types: set[str] | None = None) -> list[tuple[float, Chunk]]:
        q = tokenize(query)
        scored = []
        for chunk, doc in zip(self.chunks, self._docs):
            if doc_types and chunk.doc_type not in doc_types:
                continue
            tf = Counter(doc)
            s = 0.0
            for t in set(q):
                if t in tf:
                    f = tf[t]
                    s += self._idf.get(t, 0) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(doc) / self._avg))
            if s > 0:
                scored.append((s, chunk))
        return sorted(scored, key=lambda x: -x[0])[:k]

    def of_type(self, doc_type: str) -> list[Chunk]:
        return [c for c in self.chunks if c.doc_type == doc_type]

    def of_doc(self, doc_id: str) -> list[Chunk]:
        return [c for c in self.chunks if c.doc_id == doc_id]
