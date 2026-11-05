from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .agent import MODES, review_text
from .kb import KB
from .llm import LLM, LLMUnavailable
from .report import to_markdown

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="pmdc", description="PM Decision Copilot (synthetic LMD prototype)")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("review", help="review a proposal markdown file")
    r.add_argument("file")
    r.add_argument("--mode", choices=MODES, default=None, help="default: hybrid if credentials are set, else rules")
    r.add_argument("--kb", default=str(ROOT / "knowledge"))
    r.add_argument("--json", action="store_true")
    r.add_argument("--model", default=None)
    s = sub.add_parser("kb", help="search the knowledge base")
    s.add_argument("query")
    s.add_argument("--kb", default=str(ROOT / "knowledge"))
    s.add_argument("-k", type=int, default=5)
    e = sub.add_parser("eval", help="run the evaluation (see evals/README)")
    e.add_argument("--arms", default=",".join(MODES))
    e.add_argument("--repeats", type=int, default=2)
    e.add_argument("--cache-only", action="store_true", help="replay cached model responses; needs no credentials")
    e.add_argument("--model", default=None)
    a = p.parse_args(argv)

    if a.cmd == "kb":
        for score, c in KB.load(a.kb).search(a.query, k=a.k):
            print(f"{score:6.2f}  {c.id}  ({c.doc_type}, reviewed {c.meta.get('last_reviewed')})")
        return 0
    if a.cmd == "eval":
        from .evaluate import run_eval
        return run_eval(a.arms.split(","), a.repeats, a.cache_only, a.model)

    kb = KB.load(a.kb)
    llm = LLM(a.model)
    mode = a.mode or ("hybrid" if llm.available() else "rules")
    if a.mode is None:
        print(f"[mode: {mode}]", file=sys.stderr)
    text = Path(a.file).read_text(encoding="utf-8")
    try:
        rev = review_text(text, kb, mode, llm if mode != "rules" else None)
    except LLMUnavailable as ex:
        print(f"LLM unavailable: {ex}\nTry --mode rules for the offline path.", file=sys.stderr)
        return 2
    print(json.dumps(rev.to_dict(), indent=2) if a.json else to_markdown(rev, kb, Path(a.file).stem))
    return 0
