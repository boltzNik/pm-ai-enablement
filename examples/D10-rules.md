# Decision Readiness Review: D10

**Verdict: BLOCKED: a required policy review is not recorded.**  (mode: `rules`)

## High severity

- **MISSING_GUARDRAIL: Missing guardrails for 'Driver pay and incentives'**
  - Why: This change touches Driver pay and incentives. Required guardrails not found: Driver Hourly Earnings, Driver Safety Incident Rate, Cost Per Delivery.
  - Fix: Add each missing metric with a stop threshold.
  - Sources: `guardrail-standards#driver-pay-and-incentives`
- **POLICY_REVIEW: Legal and Compensation review not recorded**
  - Why: Triggered by: incentive, surge. No evidence of Legal and Compensation review in the document.
  - Fix: Obtain Legal and Compensation review and record the ticket reference before build.
  - Sources: `policy-compliance#driver-compensation-and-classification`
- **WEAK_EXPERIMENT_DESIGN: No validation plan**
  - Why: No experiment or staged rollout with a control was found.
  - Fix: Add a design with randomization unit, duration, MDE and stopping rule.
  - Sources: `experimentation-standards#pre-registration`

## Medium severity

- **PRIOR_ART: Overlaps EXP-021 which is not referenced**
  - Why: Matched terms: surge incentive, peak hour, peak hours. Registry says: Hypothesis: A peak-hour surge incentive increases driver acceptance.
  - Fix: Read EXP-021, state what is different this time, and reuse its learning.
  - Sources: `experiment-registry#exp-021-peak-surge-incentive`

---
Advisory pre-review only. It is not an approval and does not replace Legal, Privacy, Compliance, or Data Science review. All sources are synthetic in this prototype.
