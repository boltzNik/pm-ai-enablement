# 10. MCP servers, plugins, skills: what plugs in, where, and with what controls

> **Status labels.** *Observed* = present in the Wibey environment this prototype was built in (tool inventory at build time). *Assumed* = needed in a real deployment but not verified. **Treat every row as "assumption to verify with the platform owner"**: names, scopes, and availability change, and I did not exercise most of these connectors in the prototype. Only the CLI, the gateway call, and the Wibey skill file in this repo are actually built and run.

## 10.1 Principles
1. **Read-only first.** Every connector starts read-only. Write access is added per skill, per use case, with a named approver.
2. **Least privilege, user identity.** Calls carry the PM's identity; retrieval is filtered by that user's permissions (never filter after generation).
3. **Ownership and freshness travel with the data.** A connector that cannot supply owner and last-modified date is a weak knowledge source.
4. **Fewer, better connectors.** Each connector adds attack surface, latency, and maintenance. Add one only when a skill's eval shows it improves a decision.
5. **No standing write tools on review skills.** The reviewer never needs to write anywhere. Posting a comment on a PR or page is a separate, human-confirmed action.

## 10.2 Knowledge and context connectors (feed the reviewer)

| Capability | Component | Status | Used for | Phase | Mode | Risk and control |
|---|---|---|---|---|---|---|
| Wiki and docs (definitions, standards, policies, research) | Confluence MCP (`mcp-confluence`: search, get page, page tree, labels) | Observed | Source of metric glossary, guardrail standards, policy pages; labels as `owner`/`tier` metadata | Pilot | Read | ACL pass-through; page `last modified` used for freshness; no write |
| Tickets and initiatives | Jira MCP (`mcp-jira`: JQL search, issue read, epics) | Observed | Prior-art lookup, **ticket-ID verification of recorded reviews** (closes loophole S07), decision log items | Pilot | Read | Verify review ticket exists, correct type, correct status, and is linked to this initiative |
| Internal content search | Wibey core `content_search`, DX search (`DXIO-SERVICES`) | Observed | Cross-source discovery of Walmart-internal knowledge; Stack Overflow, GitHub | Pilot | Read | Results are untrusted text until the verifier checks them; log queries |
| Source code and config as knowledge | GEC GitHub MCP (search code, read files) | Observed | Metric definitions in code, feature-flag and experiment configs, eval repo and skill registry | Expand | Read (write only for skill registry PRs by humans) | Repo ACLs; secrets scanning; PR-only writes |
| Office documents, email, meetings | MS Graph skill (SharePoint, OneDrive, Outlook, Teams, Planner) | Observed (skill) | PRDs and decks that live in SharePoint; review-request threads | Expand | Read | Mail and chat are high-sensitivity: allow-list folders and sites, not whole mailboxes |
| Metrics and experiment data | Analytics agents (for example ClickHouse or BigQuery agents exposed through Wibey core) / experiment platform API | Assumed | Real baselines for proposals; the registry of experiments with live status | Expand | Read | Aggregate-only views; no row-level personal data; query cost limits |
| Metric layer / semantic layer | Metric store API (assumed) | Assumed | Canonical definitions as machine-readable source of truth rather than prose | Platform | Read | Single source of truth; version and owner |
| Governance systems | ServiceNow MCPs (change, incident, CMDB) | Observed | Policy review status where reviews are tracked as changes; link launches to incidents (outcome metric: regretted launches); CMDB for owner lookup | Platform | Read | Never create or approve changes from this skill |

## 10.3 Delivery and runtime (how people use it)

| Capability | Component | Status | Role | Notes |
|---|---|---|---|---|
| Agent host | Wibey (VS Code extension, CLI) | Observed | Where PMs and builders invoke skills | `integrations/wibey-skill/pm-decision-review/SKILL.md` is a working-shape skill file for this repo (not published to a registry) |
| Model access | Wibey gateway (Anthropic-compatible `/v1/messages`) | Observed (used by the prototype) | LLM calls | Token via env var; model id via `PMDC_MODEL`; swap models without code changes |
| PR review | PR Agent MCP (`pr_review`, `pr_describe`, `pr_audit`) | Observed | Review of the eval and skill code itself; pattern to copy: AI review as a comment, human decides | Used as a design reference for "advisory comment on an artifact" |
| Security and quality of the skill code | Sonar MCP, Snyk skills | Observed | Gate skill releases | Part of the skill-registry promotion checks |
| Diagrams | Mermaid renderer (`wibey-vscode`) | Observed | Architecture diagrams in docs | Docs here use Mermaid source rendered by GitHub |
| Testing | `test-orchestrator` skill, `wibey-vscode` test runner | Observed | Regression tests for the reviewer and eval-in-CI | `python3 -m unittest discover -s tests` is the minimum |

## 10.4 Skills and plugins to build or adopt (the PM skill pack)

| Skill | Source | Phase | Depends on |
|---|---|---|---|
| `pm-decision-review` (this repo) | Built | Pilot | Confluence, Jira, gateway |
| `pm-prior-art-finder` | Build | Expand | Experiment registry, Jira, Confluence |
| `pm-experiment-designer` | Build | Expand | Standards doc, metric layer |
| `pm-metric-lookup` | Build | Pilot | Glossary |
| `pm-voc-synthesizer` | Build | Expand (Red tier) | Support and feedback data, Privacy approval |
| Skill authoring and publishing | `skill-creator`, `skill-publisher`, `agent-creator` skills | Observed | Platform | How teams contribute skills to a registry, with an eval gate in front |
| Documentation publishing | `yb-library` skill | Observed | Platform | Publish playbooks and recipes to the internal library |
| Structured build pipeline | `flux` skill | Observed | Platform | For engineering teams building skills with task files and QA stages |

## 10.5 Do not connect (initially)
- Raw customer or driver tables, support transcripts with personal data, or any Red-tier source, until Privacy and Responsible AI approve a specific skill.
- Write-capable tools (create Jira issue, edit Confluence, merge PR, create or approve change) on the review skill. Humans take those actions.
- Public web search from inside the reviewer: a path for untrusted text to reach the model and for proposal text to leave the boundary.
- Any MCP server not on the approved list. Third-party MCP servers are a supply-chain risk like any dependency.

## 10.6 How these make the system efficient and productive

| Lever | Mechanism | Evidence in this repo |
|---|---|---|
| **Fewer reviewer round trips** | Pre-review catches missing baselines, guardrails, prior art, policy reviews before humans spend time | Recall by flaw type in `evals/RESULTS.md` |
| **Context built once, reused by every skill** | One owned knowledge layer behind MCP serves all skills | Same `kb.py` used by reviewer and eval |
| **Cheaper and faster calls** | Cache, tiered models, context only as large as needed | Token and latency columns per arm |
| **Trust at scale** | Verifier and citations make output checkable in seconds | Citation validity and drop counts |
| **Safe by default** | Read-only connectors, user identity, code-owned verdict | Injection pass rate |
| **Continuous improvement** | Eval-in-CI; PM overrides become new test cases; gaps become owner tickets | Stress cases and label audit |
| **Portability** | Model-agnostic client; skill is a markdown file plus CLI | `PMDC_MODEL`, `SKILL.md` |
