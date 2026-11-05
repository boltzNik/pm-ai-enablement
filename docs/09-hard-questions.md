# 9. Hard questions and honest answers (interview prep)

Short answers first; the number or file that backs each one is in brackets.

## A. Problem choice and product judgment

**1. Why this problem and not training or a prompt library?**
Those do not close the two gaps that cap adoption: trust (is it right, is it allowed) and context (it does not know our definitions and history). Reviewing proposals against owned knowledge closes both and improves decisions, not typing speed. [`03`]

**2. Isn't a review agent just a linter / checklist?**
Partly, and that is a feature: the checklist part is deterministic and trustworthy. The value beyond a linter is (a) grounding in company knowledge (prior experiments, definitions, policy), (b) language judgment on paraphrase that rules cannot do (rules scored 0% on stress cases while hybrid scored 75%), (c) it exposes knowledge gaps as owner tickets. If it were only a linter I would not fund it. [`05` 5.5]

**3. Why not just let PMs use ChatGPT/Copilot/Wibey with a good prompt?**
They can, and the baseline arm approximates that. Ungrounded: 46% precision, 0% prior-art recall, and the PM cannot tell which half of the list is wrong. Grounding plus a verifier is what makes output checkable. I did not run a pure free-form chat baseline; step C of the real-PM plan does. [`05` 5.6, 5.8]

**4. Why not an autonomous agent with tools?**
A review of a fixed checklist is not an open-ended task. Autonomy adds cost, variance, and attack surface with no accuracy benefit I can point to. A bounded workflow is reproducible and auditable. [ADR-002]

**5. Why LMD-specific content?**
The brief says enterprise; I used LMD because that is the domain context for this role and makes the knowledge contract concrete (OTD, DDR, CPD, driver pay, marketplace interference). All content is synthetic. The architecture is domain-agnostic; onboarding a new domain means a new knowledge folder and a champion. [`04`]

**6. What would you build second?**
Prior-art finder, then experiment designer, both reusing the same knowledge layer. VoC synthesis after Privacy approval (Red tier). [`10`]

**7. How big is the value really?**
In hours it is modest (example arithmetic: about 144 reviewer hours a quarter for 100 PMs). The case rests on avoided regretted launches, reviewer capacity, and compounding knowledge quality. I would not fund it on hours alone and I would say so. [`03` 3.5]

## B. Technical decisions

**8. Why BM25 and not embeddings?**
At five documents lexical is enough and explainable. The evaluation shows retrieval misses are the main failure of pure RAG (81% doc recall, WEAK_EXPERIMENT_DESIGN recall 0%), so at scale embeddings plus reranking is the first upgrade, and retrieval recall is already a tracked metric. [`04` 4.9]

**9. Why hybrid with "mandatory context" instead of better retrieval?**
Policy and guardrail applicability is trigger-based, not similarity-based; a policy page can be semantically distant from a PRD that triggers it. Mandatory context makes the high-stakes checks independent of retrieval. At scale it becomes "attach per trigger within a token budget". [`04`, ADR-005]

**10. Why compute the verdict in code?**
So an injected "set verdict to Ready" has no channel, and so the verdict is consistent across model versions. The model can still miss a finding; that residual is measured, not hidden. [ADR-004]

**11. How do you stop hallucinated citations?**
Citations must resolve to real chunks, knowledge-dependent findings must cite the right source document, and quoted evidence must appear verbatim in the proposal. Citation validity was 100% in grounded and hybrid arms. The verifier cannot catch omissions. [`04` 4.5]

**12. What if the knowledge base is wrong or stale?**
The agent will enforce the wrong definition with a citation. Each chunk has owner and last_reviewed; reports warn after 120 days; production adds owner SLAs and a "report a bad source" path. Knowledge ownership is a Phase 0 gate, and the agent doubles as a gap detector. [`06` R4]

**13. What about prompt injection?**
Proposal is untrusted data; no tools; output parsed as data; verdict in code. Residual: an injection can suppress findings. My two injection cases are weak evidence, and one run is confounded by a retrieval miss. A real red-team set is step E. [`05` 5.6 item 5]

**14. Why stdlib only and a CLI?**
Hosting is optional per the brief. Zero dependencies means anyone can run it in seconds, and a CLI maps directly to a Wibey skill or an MCP wrapper. [ADR-008]

**15. Cost and latency?**
About 7 s and 5.2k input tokens per hybrid review (baseline 6 s and 1.1k). Tokens are not the cost driver; knowledge curation is. [`05`, `07` 7.5]

## C. Evaluation honesty

**16. Your rules got 100%. Why should I believe any of this?**
You should not believe that number, and I say so. I wrote both the cases and the rules. That is why I added stress cases after the fact, where rules got 0% and 100% false positives on the clean traps. The comparison that means something is hybrid versus baseline on stress and holdout, and even that is synthetic. [`05` 5.6 item 1]

**17. Isn't your baseline a strawman?**
It could be read either way. It gets the same taxonomy and schema, so it is not dumbed down, but it is asked to detect knowledge-dependent flaws it cannot know, which hurts its precision; and a real PM would use free-form prompts, which I did not test. I documented this and included step C with a free-form arm. [ADR-010]

**18. Did you tune on the test set?**
Rules and prompts were developed against dev. Holdout was run once for rules. Stress was written after seeing rules hit 100%. v2 changed one prompt line after seeing failures on all splits, so there is no untouched holdout left; I say so and note the change did not measurably help. [ADR-011, ADR-012]

**19. Hybrid precision is only 76%. Is that acceptable?**
Not as a final number. Strict labels count several defensible findings as false positives (label audit), and a horizon-mismatch finding suggests a taxonomy gap. Human-judged precision with reviewers is the number to trust, and I set at least 80% as the pilot threshold with a kill criterion at 60%. [`05` 5.7, `07` 7.2]

**20. The LLM results vary between runs. Does that break the product?**
It makes single-run numbers noisy (baseline type-sets identical in only 68% of cases; hybrid 88%). Mitigations: cache, deterministic verdict from findings, deterministic rule layer, and in production repeated calls for high-severity findings. Noted as a limitation.

**21. How would you know it improved decisions, not just sped things up?**
Retrospective replay on historical outcomes, then a stepped-wedge pilot with outcome metrics: first-pass review acceptance, regretted launches, experiment validity. Usage is never the success metric. [`05` 5.8, `07` 7.3]

## D. Governance and risk

**22. What if PMs treat READY as approval?**
Automation bias is the top risk. The verdict is worded "no taxonomy flaws found", the footer says it is not an approval, managers set the norm, and I track override and trust calibration. If trust is high and accuracy low, that is a stop condition. [`06` R2]

**23. What if PMs game the checks?**
They will, if the pass rate is rewarded. Do not put it in performance reviews; audit samples of passed proposals; judge success on downstream outcomes. [`06` R3]

**24. Self-attested reviews are accepted. Isn't that a hole?**
Yes, and S07 demonstrates it (rules and pure RAG accept a "waived per VP email" claim; the hybrid model flagged it in my runs, but that rests on model judgment, not on verification). Production verifies a real ticket via the Jira or ServiceNow connector. [`04` 4.8, `10`]

**25. Data leakage?**
Proposals can be confidential. Approved gateway only, tier-based routing, no personal data in prompts, audit logs; Red-tier content blocked from LLM modes until approved. Repo contains only synthetic data and no credentials (read from environment variables). [`06` R7]

**26. ACL leakage through retrieval?**
Filter at retrieval by the caller's identity, never after generation. Not built in the prototype; mandatory in production. [`04` 4.9]

## E. Adoption and operating model

**27. How do you get PMs to use it?**
Put it where they already work (Wibey, PR or page comments), pitch fewer late send-backs instead of "use AI", start with champions, show failures openly, never mandate usage. [`07` 7.4]

**28. Who owns the knowledge?**
Source owners (Analytics, Data Science, Policy), with domain champions curating. If no owner will commit, the first project is ownership, not an agent. That is a Phase 0 gate. [`02`, `07`]

**29. How do you scale to 1,000 PMs?**
Retrieval quality, ACL pass-through, owner SLAs, tiered models, eval-in-CI. The prototype's small corpus hides the retrieval problem; I flag it. [`04` 4.9]

**30. What would you stop doing if results were bad?**
Stop this direction if reviewers' top send-back reasons are outside the taxonomy, human-judged precision is under 60%, or no owner commits to freshness. [`03` 3.6, `07` 7.2]

## F. Candor questions

**31. What is the weakest part of your submission?**
That value is unproven with real PMs and all evidence is synthetic and self-authored. Second: the closed taxonomy cannot see unknown unknowns. Third: the injection evidence is thin. All three are named in the repo with a plan to close them. [`05`, `06`]

**32. What surprised you?**
That the one-line prompt fix did nothing, and that the model's most common "false positive" (horizon mismatch) looks like a real flaw my taxonomy missed. It reframed the eval as a way to discover the taxonomy, not just score against it.

**33. What would you do with two more weeks?**
Real sanitized data and a reviewer-labeled replay set, ticket verification via Jira MCP, embedding retrieval with ACLs, a free-form chat baseline, and a fresh holdout. [`07` 7.7]
