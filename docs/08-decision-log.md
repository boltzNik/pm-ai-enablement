# 8. Decision log (ADR style)

Each entry: context, decision, alternatives considered, consequence. Written so the "why this and not that" is defensible in conversation.

### ADR-001: Build a reviewer, not a writer
- **Context**: Most "AI for PM" demos generate PRDs. Generation is the step that is already fast and is commodity in any chat tool.
- **Decision**: Review proposals against enterprise knowledge.
- **Alternatives**: PRD generator; chat-with-docs bot; usage dashboard; policy bot (`03`).
- **Consequence**: Smaller surface area, safer failure mode (a miss equals today's status quo), measurable with planted flaws. Cost: less "wow" in a demo.

### ADR-002: Bounded workflow, not an autonomous agent
- **Decision**: Fixed pipeline (parse, retrieve, check, model, verify, verdict).
- **Alternatives**: tool-calling loop where the model decides what to search; multi-agent debate.
- **Consequence**: Reproducible and auditable, cheaper, no runaway behavior. Cost: cannot handle open-ended questions. Acceptable, because the job is a checklist-shaped review.

### ADR-003: Closed taxonomy of seven flaw types
- **Decision**: Fixed, enumerated flaw types, each with a definition.
- **Alternatives**: free-form critique.
- **Consequence**: Measurable precision and recall, consistent output, easy routing to owners. Cost: blind to anything outside the list (loophole 1 in `06`). Taxonomy must be validated and grown from reviewers' real send-backs.

### ADR-004: Severity and verdict computed in code
- **Decision**: A table maps flaw type to severity; policy flaw means BLOCKED.
- **Alternatives**: ask the model to judge severity and verdict.
- **Consequence**: Injection cannot flip the verdict; consistent across model versions. Cost: crude severity; same type always same severity.

### ADR-005: Hybrid grounding (retrieval + mandatory context + rule candidates)
- **Context**: Pure RAG missed policy chunks in the evaluation (retrieval doc recall below 100%).
- **Decision**: Attach triggered guardrail and policy sections, glossary, and standards always; supply rule findings as candidates.
- **Alternatives**: pure RAG; stuff the whole corpus (does not scale); fine-tune (stale, no provenance).
- **Consequence**: Higher recall and verdict accuracy in the eval, larger prompt (see token columns). At scale "always attach" must become "attach per trigger" with a size budget.

### ADR-006: Verifier between model and user
- **Decision**: Drop findings with unknown type, unverifiable quote, unresolved citation, or missing grounding for knowledge-dependent types.
- **Consequence**: Citation validity measured at 100% in grounded arms; zero fabricated sources reach the user. Trade-off: the grounding gate converts a retrieval miss into a missed finding (visible in grounded-llm, see `05`). Verifier cannot detect omissions.

### ADR-007: Synthetic, labeled knowledge and cases
- **Decision**: All corpus and cases invented, marked synthetic; no internal URLs, names, or numbers.
- **Alternatives**: sanitized real data (needs approvals and time); public datasets (not LMD-shaped).
- **Consequence**: Safe to submit and share; demonstrates the knowledge contract (owner, freshness, aliases, triggers). Cost: results are not evidence of production quality.

### ADR-008: Standard library only, CLI first
- **Decision**: Zero dependencies, `python -m pmdc`.
- **Alternatives**: web app, framework (LangChain, etc.), vector DB.
- **Consequence**: Runs anywhere in seconds, readable, auditable. The brief says hosting is optional; the CLI maps directly to a Wibey skill or MCP wrapper. Cost: no UI polish.

### ADR-009: Evaluate four arms with three splits and cached replay
- **Decision**: rules, baseline-llm, grounded-llm, hybrid; dev, holdout, stress splits; model responses cached to disk.
- **Alternatives**: single score; LLM-as-judge.
- **Consequence**: Ablation shows what each layer buys; splits expose overfitting; cache makes results replayable without credentials. No LLM-as-judge: labels are structural (flaw types), so scoring is exact-match on type, which avoids judge bias.

### ADR-010: Define the baseline honestly
- **Decision**: The baseline LLM gets the same taxonomy and schema but no knowledge.
- **Why**: Comparing against a deliberately dumb prompt flatters the system. This isolates grounding.
- **Known weakness**: A real PM would not use my taxonomy; the baseline here is stronger than "paste PRD into chat and ask for feedback" on structure, and weaker on knowledge-dependent types it cannot know. A free-form baseline scored by reviewers is the right next experiment (`05` section 5.8).

### ADR-011: Add stress cases after rules hit 100%
- **Context**: Rules scored 100% on dev and holdout cases because the author wrote both.
- **Decision**: Write cases to defeat keyword rules (paraphrase, synonyms, false-positive traps, self-attested waiver) and report them separately.
- **Consequence**: Shows the failure boundary and justifies the model layer on evidence. Disclosed as post-hoc.

### ADR-012: Prompt iteration policy (v1 to v2)
- **Context**: v1 results showed the model emitting findings that its own text said were not flaws.
- **Decision**: One generic prompt rule added ("never emit a finding you conclude is not a flaw"); v1 results preserved next to v2.
- **Consequence**: Transparent change history. Caveat: v2 was informed by failures on dev, holdout and stress, so there is no untouched holdout left. A fresh holdout is required before any claim beyond "directionally better".

### ADR-013: No memory, no dialogue, no learning in v1
- **Decision**: Single-turn, stateless.
- **Consequence**: Reproducibility. Next data source for improvement is PM overrides, which needs UI and identity (production scope).
