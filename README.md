# PM Decision Copilot: AI enablement for Product Managers (LMD)

Home assignment: *Staff PM, AI Enablement*. One repository containing the strategy, the ecosystem design, a **runnable prototype**, its evaluation, and the path to enterprise adoption.

> **Everything in `knowledge/` and `evals/cases/` is synthetic.** No real Walmart data, names, URLs, or credentials are in this repo. Results are evidence the pipeline works, not evidence of production value (see `docs/05-evaluation.md`).

## The answer in one paragraph
AI adoption among PMs stalls on a **trust gap** (is it right? is it allowed?) and a **context gap** (it does not know our metric definitions, past experiments, or policies), not on tool access. I chose the hardest, highest-leverage problem on that journey: **proposals reach scarce human reviewers with preventable gaps**. The prototype is a **grounded decision-readiness reviewer**: it checks a proposal against owned enterprise knowledge, returns cited findings and a verdict computed in code (never by the model), and never approves anything. I evaluated it against an ungrounded baseline, found where each layer fails, and wrote down how to test it with real PMs.

## Map to the brief
| Brief item | Where |
|---|---|
| 1. What AI-native PM means | `docs/01-ai-native-pm.md` |
| 2. Ecosystem (tools, agents, skills, data, governance, training, measurement) and operating model | `docs/02-ecosystem-and-operating-model.md`, `docs/10-mcp-and-plugin-catalog.md` |
| 3. Hardest, highest-value problem; alternatives considered | `docs/03-problem-selection.md` |
| 4. Working agent | `pmdc/` (code), `docs/04-architecture.md` |
| 5. Baseline, test cases, results, failures, real-PM test plan | `docs/05-evaluation.md`, `evals/RESULTS.md` |
| Risks, loopholes, governance | `docs/06-risks-and-governance.md` |
| Path to enterprise adoption | `docs/07-adoption-roadmap.md` |
| Why each decision | `docs/08-decision-log.md` |
| Interview prep: hard questions | `docs/09-hard-questions.md` |
| AI-native working approach (how this was built) | `docs/11-ai-native-working-approach.md` |

## Quickstart (Python 3.10+, no dependencies; run from the repo root)
```bash
# 1. Tests (offline)
python3 -m unittest discover -s tests

# 2. Review a proposal offline (deterministic rules, no credentials)
python3 -m pmdc review evals/cases/D10.md --mode rules

# 3. Review with the model (hybrid = proposed system)
export ANTHROPIC_AUTH_TOKEN=...          # or ANTHROPIC_API_KEY
export ANTHROPIC_BASE_URL=...            # optional, an Anthropic-compatible gateway
export PMDC_MODEL=claude-sonnet-5-5      # optional, any model your endpoint serves
python3 -m pmdc review evals/cases/D10.md --mode hybrid

# 4. Reproduce the evaluation tables without credentials (replays cached model responses)
python3 -m pmdc eval --cache-only        # regenerates evals/RESULTS.md

# 5. Re-run the evaluation live (about 150 model calls)
python3 -m pmdc eval

# Other
python3 -m pmdc kb "peak incentive for drivers"    # search the knowledge base
```
Behind a corporate proxy with a custom CA, set `PMDC_CA_BUNDLE` (or `SSL_CERT_FILE`) to the CA bundle path.

Review your own proposal: copy the structure of `evals/cases/D01.md` (headings: Problem, Proposal, Success Metrics, Guardrail Metrics, Experiment Plan, Reviews And Dependencies) and run `python3 -m pmdc review yourfile.md`.

## Results at a glance (from `evals/RESULTS.md`, 25 synthetic cases, 2 repeats)
| Arm | Precision | Recall | Verdict accuracy | Stress-split F1 |
|---|---|---|---|---|
| rules only | 81% | 81% | 72% | **0%** (100% on cases I wrote) |
| baseline LLM (no knowledge) | 46% | 83% | 78% | 47% |
| grounded LLM (pure RAG + verifier) | 86% | 70% | 72% | 47% |
| **hybrid (proposed)** | 76% | **98%** | **90%** | **75%** |

Honest reading: grounding clearly helps on company-specific flaws (prior art: 0% without knowledge, 100% with); pure RAG loses recall when retrieval misses; hybrid recovers it at about 2x tokens and some extra speculative findings. All of this is synthetic and self-authored; the real test is `docs/05-evaluation.md` section 5.8.

## Repository layout
```
knowledge/            synthetic enterprise knowledge (glossary, guardrails, policy, experiment standards, experiment registry)
pmdc/                 prototype: kb.py (chunks + BM25), prd.py, checks.py (7 deterministic checks), agent.py (modes + verifier),
                      llm.py (stdlib client + disk cache), evaluate.py, report.py, cli.py, types.py
evals/cases/          25 synthetic proposals with planted flaws (dev D*, holdout H*, stress S*)
evals/labels.json     ground truth
evals/RESULTS.md      generated results (v2); evals/results/RESULTS-v1.md = before the one prompt change
evals/results/cache/  cached model responses, so results replay without credentials
examples/             sample reports (rules, hybrid, injection, waiver)
integrations/         Wibey skill file for the reviewer
docs/                 strategy, architecture, evaluation, risks, roadmap, decisions, Q&A, MCP catalog
tests/                12 unit tests
```

## Assumptions
- LMD = Last Mile Delivery. Metric names, policies, experiments, and owners are invented placeholders shaped like real ones.
- Scale assumptions in `docs/03` and `docs/07` (PM counts, send-back rates, thresholds) are illustrative and must be replaced with discovery data.
- The MCP and plugin catalog (`docs/10`) labels what I observed in the Wibey environment versus what is assumed; only the CLI, gateway call, and skill file were actually run.

## Limits (stated up front)
Synthetic data; single author for cases, rules and labels; small n; one model; no real PMs yet; closed taxonomy; weak injection evidence. Details and the plan to close each: `docs/05-evaluation.md`, `docs/06-risks-and-governance.md`.
