# Decision Readiness Review: D10

**Verdict: BLOCKED: a required policy review is not recorded.**  (mode: `hybrid`)

## High severity

- **MISSING_GUARDRAIL: Required pay/incentive guardrails absent**
  - Why: The proposal introduces a surge incentive (driver pay lever) but only guards neighboring-zone acceptance. Driver Hourly Earnings, Driver Safety Incident Rate, and Cost Per Delivery are all missing.
  - Evidence: "Driver Acceptance Rate in neighboring zones: should not drop."
  - Fix: Add Driver Hourly Earnings, Driver Safety Incident Rate, and Cost Per Delivery as guardrails with explicit stop thresholds.
  - Sources: `guardrail-standards#driver-pay-and-incentives`
- **POLICY_REVIEW: No Legal and Compensation review recorded**
  - Why: A surge incentive is a driver pay change that triggers the compensation policy, which requires Legal and Compensation review. The proposal states there are no reviews.
  - Evidence: "## Reviews And Dependencies None."
  - Fix: Obtain and record Legal and Compensation review before launch.
  - Sources: `policy-compliance#driver-compensation-and-classification`
- **WEAK_EXPERIMENT_DESIGN: No experiment plan; full rollout with no control**
  - Why: The plan is a full rollout across all markets with dashboard monitoring. There is no control, no market/switchback design, no duration of at least 14 days, no MDE/power, and no stopping rule. Pay changes cause marketplace interference.
  - Evidence: "None. We will roll out to all markets and monitor the dashboard."
  - Fix: Run a market-level or switchback test of at least 14 days with pre-registered primary metric, MDE, power, and stopping rule.
  - Sources: `experimentation-standards#marketplace-interference`, `experimentation-standards#pre-registration`, `experimentation-standards#duration-and-seasonality`

## Medium severity

- **PRIOR_ART: Repeats EXP-021 without referencing it**
  - Why: EXP-021 tested a peak-hour surge incentive and found adjacent-zone interference and a cost increase. The proposal neither cites it nor applies its learning (market/switchback design, track neighbors).
  - Evidence: "Launch a surge incentive during peak hours across all markets and watch the dashboard."
  - Fix: Reference EXP-021, explain what differs, and adopt its learnings: market or switchback design, neighbor tracking, and cost monitoring.
  - Sources: `experiment-registry#exp-021-peak-surge-incentive`

---
Advisory pre-review only. It is not an approval and does not replace Legal, Privacy, Compliance, or Data Science review. All sources are synthetic in this prototype.
