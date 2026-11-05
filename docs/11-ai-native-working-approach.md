# 11. How this was built: the AI-native working approach

The brief asks for an AI-native way of working, so this records how AI was used on this assignment, what stayed human, and which controls kept the result honest.

## Division of labor
| Work | AI (Wibey, Claude) | Human owner (the PM) |
|---|---|---|
| Problem framing and choice | Generated and scored alternatives; stress-tested the ranking with a sensitivity check | Chooses the problem, owns the weights and the judgment |
| Strategy docs (01-03, 06, 07) | Drafted structure and tables | Owns every claim; reviews against real LMD context; replaces illustrative assumptions with discovery data |
| Prototype code and tests | Wrote and refactored code; debugged (plural matching, empty-split scoring) | Reviews, runs, and can explain every module |
| Evaluation design | Proposed arms, splits, metrics | Decides what counts as success and the pre-registered thresholds |
| Failure analysis | Surfaced model disagreements for audit | Adjudicates which disagreements are label errors, taxonomy gaps, or model errors |
| Final claims | None | Owns them |

## Controls that kept AI output honest
1. **Independent review before building and before finishing.** A second, stronger reviewer model critiqued the plan and the deliverable. Its changes included: use a real LLM baseline instead of a rules-only strawman; write labels before tuning; keep the corpus synthetic; add a decision log and hard-questions doc.
2. **Labels written before any model ran.** `evals/labels.json` was fixed first; results are never edited.
3. **Numbers come from the runner.** `evals/RESULTS.md` is generated; docs quote it.
4. **Failures were investigated, not explained away.** Example: I first read the pure-RAG injection miss as "the model obeyed the injection". Reading the retrieved context showed no policy chunk was retrieved, so the claim was rewritten as confounded (`05` 5.6 item 5).
5. **Changes are versioned in the open.** The one prompt change is documented, v1 results are preserved (`evals/results/RESULTS-v1.md`), and the note says it did not help.
6. **Reproducibility checks.** Fresh-copy run of tests, offline review, and `eval --cache-only` with credentials unset, which regenerates identical numbers; a scan for credentials and internal hostnames found none.
7. **Disclosure of post-hoc work.** Stress cases were written after rules hit 100%; the label audit lists defensible disagreements without changing labels.

## Habits this models for other PMs
- Delegate drafts and checks, verify claims against primary sources, own the decision.
- Ask the tool to critique the plan, then check the critique against evidence.
- Keep the evaluation set and its history as a team asset.
- Say what is unproven.
