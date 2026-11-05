# 7. Path to enterprise adoption

## 7.1 Phases and gates

| Phase | Timing (assumed) | Scope | Exit gate (all must hold) |
|---|---|---|---|
| **0. Discover and baseline** | Weeks 0-3 | 8-10 PM and 4-5 reviewer interviews; pull last 30 initiatives; confirm owners for glossary, registry, policy; capture baseline review cycle time and send-back reasons | Taxonomy validated against real send-back reasons; named owners for each source; baseline measured |
| **1. LMD pilot** | Weeks 4-12 | 12-20 LMD PMs; real knowledge connectors (read-only) for 2 sources first; Wibey skill; weekly office hours | Reviewer-agreement and time-saved targets below; zero data-handling incidents; PM trust score at or above the target |
| **2. Expand** | Months 4-6 | 2 more domains; +2 skills (prior-art finder, experiment design assistant); champions network; fast-lane governance | Adoption and quality hold in new domains without a custom-built knowledge base; cost per review within budget |
| **3. Platform** | Months 7-12 | Skill registry open to teams; eval-in-CI; operating model fully staffed | Third-party skills pass the eval gate; measurable decision-quality lift versus matched control teams |

## 7.2 Pilot success criteria (pre-registered, assumed thresholds to be set with stakeholders)

| Metric | Target | How measured |
|---|---|---|
| Reviewer agreement: share of agent findings reviewers judge valid | at least 80% | Reviewers label each finding valid / not valid / valid but low value |
| Recall on reviewer send-backs: share of issues human reviewers raised that the agent also raised | at least 60% on taxonomy types | Replay of 30-50 historical proposals |
| Clean-doc false-positive rate | at most 20% | Reviewer labels on proposals that passed review without changes |
| First-pass review acceptance | +15 points versus baseline | Stepped rollout (see 7.3) |
| Review cycle time | -20% | Same |
| PM trust calibration | Trust matches measured accuracy (neither blind trust nor ignoring) | Short survey plus override rate |
| Safety | 0 incidents of restricted data in prompts | Audit log review |

**Kill or re-scope criteria**: reviewer agreement under 60%, or recall under 40% after one tuning cycle, or no owner commits to knowledge freshness, or PMs stop opening reports after week 4 despite reminders.

## 7.3 How to prove it worked (causality, not anecdotes)
- **Stepped-wedge rollout**: teams start in randomized order; early teams are treated, later teams are the control for the same period. This controls for seasonality (peak season changes everything in last mile).
- **Retrospective replay**: run the agent on historical proposals with known outcomes (shipped and failed; shipped and succeeded; killed) and measure whether flagged flaws preceded failures. Cheap, fast, and the best first evidence.
- **Outcome tracking**: regretted launches (post-launch guardrail breaches), experiment validity rate, reviewer hours per launch.

## 7.4 Change management
- **Start where the pain is**: reviewers and PMs both dislike late send-backs. Pitch is "fewer surprises", not "use AI".
- **Champions** per domain own local knowledge and recipes; their feedback goes into the weekly triage.
- **Make the compliant path the easy path**: skill inside the tools PMs already use; one-page policy; 5-day fast lane.
- **Manager norms**: managers ask "what did the review find and what did you do about it", not "did you use AI".
- **Do not mandate usage or use pass rate in performance**: this is how gaming begins (risk R3).
- **Communicate failures**: publish the eval's failing cases and what changed. Trust is built by showing where it fails.

## 7.5 Team and cost (assumptions)
- Pilot team: 1 PM (owner), 2 engineers, 0.5 data scientist (evals), 1 domain champion at 10-20%, part-time Privacy/InfoSec liaison.
- Run cost per review: see token and latency columns in `evals/RESULTS.md` for the measured per-review tokens; multiply by volume (about 600 proposals per quarter in the sizing example). At current gateway pricing this is a rounding error next to people time; the real cost is **knowledge curation**, not tokens. Budget for it explicitly.

## 7.6 Dependencies and what could stall this
| Dependency | Risk | Mitigation |
|---|---|---|
| Source owners (Analytics, Data Science, Policy) | No bandwidth, no ownership | Make owner sign-off a Phase 0 gate; use agent-found gaps as concrete tickets |
| Gateway and approved model access | Delays, quotas | Start in the existing approved path; model-agnostic client |
| Privacy and InfoSec | Review latency | Early engagement; Amber tier design; no personal data in the pilot |
| Connector availability | Source systems lack APIs or MCP | Start with exports (markdown) and the connectors already available (Confluence, Jira, GitHub) |
| PM time | Change fatigue | Embed in the existing review step; no new meeting |

## 7.7 If I had two more weeks
1. Replace synthetic corpus with a sanitized slice of real LMD definitions and 20 real historical proposals (with approval).
2. Build the real-PM replay and reviewer-labeling harness.
3. Ticket-ID verification for policy reviews via the Jira MCP.
4. Embedding retrieval plus ACL filtering; track retrieval recall as a first-class metric.
5. Wibey skill packaging and a PR-comment integration so reviews appear where reviewers already work.
