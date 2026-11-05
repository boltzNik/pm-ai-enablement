# 1. What "AI-native PM" means

## Position
An AI-native PM is not a PM who writes documents faster. It is a PM whose **decision system** is redesigned around AI: evidence is gathered, challenged, and traced by machines at low marginal cost, and the human spends their time on judgment, trade-offs, and stakeholder alignment, which stay human.

Speed of document creation is the weakest benefit and the most dangerous one. A faster PRD factory fed by weak inputs produces more plausible-looking bad decisions per week. The test of AI-native work is: **did the decision get better, or just arrive sooner?**

## The three outcome lenses (what AI must improve)

| Lens | What improves | Leading indicators (weeks) | Lagging indicators (quarters) |
|---|---|---|---|
| **Product decisions** | Evidence quality, counterfactual thinking, use of prior learning | % proposals with defined metric + baseline + guardrails before review; % that cite prior experiments; reviewer "send-backs" per proposal | Experiment win rate; reversal rate of launched decisions; regretted launches (guardrail breaches post-launch) |
| **Team effectiveness** | Time from question to decision, rework, knowledge reuse | Review cycle time; first-pass review acceptance; discovery-to-decision lead time; reuse of shared skills and context | Roadmap predictability; onboarding time for new PMs; reviewer load (Legal, Data Science) per shipped initiative |
| **Business outcomes** | Impact per unit of PM and engineering effort | Share of roadmap tied to canonical metrics | LMD outcomes the PM portfolio is accountable for: on-time rate, defect rate, cost per delivery, driver earnings and safety, CSAT |

Usage metrics (logins, prompts, seats) are inputs. They are never the outcome, and optimizing them invites Goodhart behavior (people prompt more, decide no better).

## Behaviors that define the role

1. **Evidence before eloquence.** Every claim in a decision memo is traceable to a source or labeled as an assumption. AI output without a citation is a hypothesis, not a fact.
2. **Delegate, verify, own.** Delegate retrieval, synthesis, first drafts, checklist review, and simulation to AI. Verify anything that changes a decision. Own the call and the consequences. Accountability never moves to the tool.
3. **Shift review left.** Use AI as a cheap pre-reviewer so scarce human reviewers (Legal, Privacy, Data Science, Ops) see better inputs and spend time on real judgment, not on missing baselines.
4. **Reuse over reinvent.** Prompts, skills, eval sets, and curated context are team assets, versioned and improved, not personal tricks.
5. **Evaluate before trusting.** A new AI workflow gets a baseline, test cases, and known failure modes before it touches a real decision. "It felt good in the demo" is not evidence.
6. **Know the risk tier.** Green (public, low stakes) vs amber (internal data, advisory output) vs red (customer or driver personal data, pay, safety, regulated). The tier decides tools, review, and logging.
7. **Measure outcomes, not activity.**

## Maturity ladder (used to design enablement and measure progress)

| Level | Description | Typical behavior | What moves a PM up |
|---|---|---|---|
| L0 Unaware or avoiding | No usage, fear or uncertainty | None | Safe sandbox, clear policy, peer proof |
| L1 Tourist | Occasional chat use for text | Rewrites emails, summarizes docs | Role-specific recipes tied to a real task |
| L2 Assisted | Regular use inside one workflow | Drafts PRDs, synthesizes research | Grounding in enterprise context; verification habits |
| L3 Trusted | Uses grounded, evaluated workflows for decisions | Pre-review agents, metric lookup, prior-art check | Shared skills, eval sets, governance clarity |
| L4 Redesigned | Changes how the team works | Decision memo review loop, AI-assisted experiment design, portfolio analytics | Org-level operating model, incentives |

The enterprise problem is that the population is stuck at L1: tools exist, but nothing turns tourist use into trusted use. The prototype in this repo targets the L2 to L3 transition, because that is where trust, context, and governance become the binding constraints.

## Anti-patterns to name explicitly
- **AI slop**: fluent, uncited, generic strategy text that nobody checks.
- **Automation bias**: accepting the tool's "looks fine" as approval.
- **Context-free prompting**: results generic because the model never saw LMD metric definitions or past experiments.
- **Shadow AI**: PMs pasting driver or customer data into unapproved tools because the approved path is slower.
- **Metric theater**: counting seats and prompts as success.
- **Governance as a blocker**: policy so vague or slow that the compliant path is the hard path.
