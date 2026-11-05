---
id: guardrail-standards
type: standard
owner: SYNTHETIC - LMD Product Operations (placeholder owner)
last_reviewed: 2026-08-01
sensitivity: synthetic-demo
---
# Guardrail Metric Standards (SYNTHETIC)

Every proposal that changes behavior in an area below must list the required guardrail metrics, with a stop threshold, alongside its primary metric.

## ETA And Delivery Promise Changes
category: ETA and delivery promise
trigger_terms: eta; delivery promise; promise window; delivery window; time slot; promise windows
required_guardrails: Delivery CSAT; Contact Rate; Promise Accuracy
Rationale: Tightening or padding promises moves on-time rate without changing real speed. Guardrails catch customer harm and conversion side effects.

## Driver Pay And Incentives
category: Driver pay and incentives
trigger_terms: driver pay; incentive; incentives; bonus; surge; payout; earnings; pay rate
required_guardrails: Driver Hourly Earnings; Driver Safety Incident Rate; Cost Per Delivery
Rationale: Pay levers can raise acceptance while raising cost or encouraging unsafe speed. Earnings floor and safety must not regress.

## Routing Dispatch And Batching
category: Routing, dispatch and batching
trigger_terms: batching; batch; routing; dispatch; route; stacking; assignment algorithm
required_guardrails: On-Time Delivery Rate; Delivery Defect Rate; Driver Safety Incident Rate
Rationale: Efficiency gains from batching or routing often trade off against lateness and defects in dense zones.

## Customer Communication And Notifications
category: Customer communication
trigger_terms: notification; notifications; push; sms; nudge; tracking page; chatbot
required_guardrails: Contact Rate; Delivery CSAT
Rationale: Messaging changes can reduce contacts short term but create fatigue and opt-outs.

## Proof Of Delivery And Handoff
category: Proof of delivery and handoff
trigger_terms: proof of delivery; delivery photo; handoff; leave at door; contactless; signature; id verification
required_guardrails: Delivery Defect Rate; Contact Rate; Delivery Completion Rate
Rationale: Handoff changes alter claims, time per stop, and failed deliveries.
