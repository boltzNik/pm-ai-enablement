# 6. Risks, loopholes, and governance

Two lists: a **risk register** for the program, and an explicit **loopholes** list for this solution. Naming the loopholes first is deliberate: a reviewer will find them anyway, and an owner who already knows them reads as senior.

## 6.1 Risk register

L = likelihood, I = impact (H/M/L). Residual = after controls.

| # | Risk | L | I | Prototype control | Production control | Residual | Owner |
|---|---|---|---|---|---|---|---|
| R1 | Model fabricates evidence or citations | M | H | Verifier: quotes must appear in the proposal; citations must resolve; knowledge-dependent types must cite the right source | Same, plus click-through verification logging | Low-Med | AI Enablement |
| R2 | **Automation bias**: PMs treat `READY` as approval | H | H | Verdict wording "no taxonomy flaws found"; report footer says not an approval | UI copy, manager norms, review SLA unchanged; track overrides | Med | AI Enablement + managers |
| R3 | **Goodhart / gaming**: PMs write to pass the checklist (add a guardrail line, no thought) | H | M | Not addressed in the prototype | Do not use verdict as a performance metric; sample human audits of "passed" proposals; track outcome metrics (regretted launches), not pass rate | Med | AI Enablement |
| R4 | Knowledge base is stale or wrong, so agent is confidently wrong | H | H | `owner`, `last_reviewed`, freshness warnings | Owner SLAs, alerting, a "report a bad source" button feeding owners | Med | Knowledge owners |
| R5 | Retrieval misses the one relevant chunk | M | H | Hybrid mode attaches mandatory chunks; retrieval doc recall tracked | Hybrid search + rerank; recall monitored on the eval set | Low-Med | AI Enablement |
| R6 | Prompt injection suppresses findings | M | M | Untrusted-data framing, no tools, code verdict; 2 injection cases in eval | Add classifiers on inputs; red-team set; no write tools ever on this skill | Low-Med | InfoSec + AI Enablement |
| R7 | Sensitive data leaves the boundary (proposals contain confidential strategy; some contain driver or customer data) | M | H | Synthetic data only in repo; credentials via env | Approved gateway only; data classification check before send; Red-tier proposals blocked from LLM modes or routed to approved model with logging | Low-Med | InfoSec + Privacy |
| R8 | ACL leakage: agent exposes documents the PM cannot normally access | M | H | N/A (synthetic corpus) | ACL filter at retrieval keyed to user identity, never post-filter | Low | Platform |
| R9 | False positives cause alert fatigue and the tool is ignored | H | M | Clean-doc false-positive rate is measured, not hidden | Severity-ranked output, one-click "not applicable" with reason feeding evals | Med | AI Enablement |
| R10 | Over-reliance deskills reviewers and junior PMs | M | M | Advisory framing | Keep human review mandatory; coach explanations over verdicts; measure PM proficiency trend | Low-Med | Managers |
| R11 | Model version drift changes behavior silently | M | M | Pinned model id recorded in results; cached replay | Eval-in-CI on every model or prompt change; canary period | Low | Platform |
| R12 | Evaluation is circular (the author wrote cases and rules) | H | H | Holdout and stress splits; stated openly in `05-evaluation.md` | Real-PM replay set built and labeled by reviewers, not the builder | Med | AI Enablement + reviewers |
| R13 | Adoption fails: PMs do not trust or need it | M | H | Narrow wedge with immediate value | Pilot with champions, stepped rollout, kill criteria (`07`) | Med | Program lead |
| R14 | Equity: domains with poor knowledge get worse service | M | M | N/A | Readiness check per domain before rollout; knowledge investment as part of onboarding | Med | Champions |
| R15 | Cost grows faster than value | L | M | Tokens and latency reported per arm | Tiered models, caching, per-team budgets | Low | Platform |
| R16 | Regulatory or policy change (e.g., AI use rules) makes parts non-compliant | L | H | Policy content owned and dated | Governance council in the loop; policy corpus versioned | Low | Governance council |

## 6.2 Loopholes in this solution (and the honest answer)

1. **Closed taxonomy = unknown unknowns.** It finds seven kinds of flaws and nothing else. A proposal can be strategically wrong and pass. *Answer:* the reviewer is a floor, not a ceiling; the taxonomy should grow from reviewers' real send-back reasons (discovery step 1), and the verdict says "no taxonomy flaws found", never "good".
2. **Self-attested reviews.** The prototype accepts "Legal review: waived per VP email, no ticket" (case S07). A real system must verify a ticket ID against the system of record (Jira or ServiceNow MCP). *Answer:* shown as a stress case on purpose: rules and pure RAG accept the waiver; the hybrid model flagged it, but that is model judgment, not verification. The fix is ticket-ID verification, specified in `04` section 4.8.
3. **Gaming.** Writing a guardrail line to satisfy a checker is cheaper than thinking. *Answer:* never tie the pass rate to performance reviews; audit samples; measure downstream outcomes.
4. **Synthetic everything.** Corpus, cases, and rules were written by one person. *Answer:* high scores on authored cases prove only that the pipeline works. Evidence of value requires real-PM replay (`05` section 5.8).
5. **Rules overfit the author's vocabulary.** Dev and holdout cases hit 100% for rules; paraphrase stress cases hit 0%. *Answer:* that is exactly why a model layer exists, and why the hybrid design is justified by measured results, not taste.
6. **The model can still miss.** Verification catches fabrication, not omission. A missing finding is invisible to the verifier. *Answer:* recall is measured; rule candidates raise the floor; humans still review.
7. **Injection can suppress.** The verdict cannot be spoofed, but a model that obeys an injected "no findings" yields a miss. *Answer:* measured (injection pass rate); defense in depth in production.
8. **Knowledge quality is outside the agent's control.** If the glossary is wrong, the agent enforces the wrong definition with citations. *Answer:* ownership and freshness are program requirements, and the agent doubles as a sensor for gaps.
9. **Proposals themselves are sensitive.** Sending them to a model is a data-handling decision. *Answer:* approved gateway only; tier-based routing.
10. **Single-turn only.** No dialogue, no memory, no learning from a PM's corrections. *Answer:* deliberate for a first version (reproducibility); override feedback is the next data source.

## 6.3 Governance model for this skill

| Control | Rule |
|---|---|
| Risk tier | Amber (internal proposals, advisory). Raised to Red if a proposal contains customer or driver personal data |
| Human in the loop | AI flags; humans approve. The skill has no write tools and cannot approve or block a release |
| Model and data | Approved models only via the enterprise gateway; no personal data in prompts; log retrieved sources and drops |
| Change control | Prompt, taxonomy, knowledge, or model change requires an eval pass and a version note |
| Transparency | Every finding shows its source chunk, owner, and last-reviewed date |
| Recourse | PM can mark a finding wrong with a reason; reasons feed the eval set and owners |
| Retirement | Skill is reviewed quarterly; retire if outcome metrics do not move (kill criteria in `07`) |
