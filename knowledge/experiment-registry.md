---
id: experiment-registry
type: experiment
owner: SYNTHETIC - LMD Data Science (placeholder owner)
last_reviewed: 2026-09-01
sensitivity: synthetic-demo
---
# Experiment Registry (SYNTHETIC - invented results)

## EXP-014 ETA Buffer
keywords: eta buffer; promise window; promise windows; padding; delivery window; buffer
status: concluded - not shipped
Hypothesis: Adding a 10-minute buffer to promised windows raises on-time rate.
Result: On-Time Delivery Rate +3.1 pts, but checkout conversion -1.2% and Delivery CSAT flat. Gain came from relaxed promises, not faster delivery.
Learning: Judge promise changes on Promise Accuracy and conversion, not on OTD alone.

## EXP-021 Peak Surge Incentive
keywords: surge incentive; peak pay; driver bonus; peak hour; peak hours; surge pay
status: concluded - shipped in 2 markets
Hypothesis: A peak-hour surge incentive increases driver acceptance.
Result: Driver Acceptance Rate +6 pts, Cost Per Delivery +$0.42. Adjacent zones lost drivers and OTD fell there (interference), so zone-level A/B overstated the lift.
Learning: Test pay changes with market or switchback designs and track neighbors.

## EXP-027 Auto Batching
keywords: batching; auto-batching; stacking; multi-order; orders per trip; three orders
status: concluded - shipped with density cap
Hypothesis: Batching up to three orders per trip lowers cost.
Result: Orders Per Trip +0.4 and Cost Per Delivery -4%, but On-Time Delivery Rate -2.2 pts and Delivery Defect Rate +0.3 pts in dense zones.
Learning: Cap batch size by zone density and track OTD and DDR.

## EXP-031 Proof Of Delivery Photo
keywords: proof of delivery; delivery photo; handoff photo; not received; photo
status: concluded - shipped for high-value orders
Hypothesis: Mandatory delivery photos reduce not-received claims.
Result: Not-received claims -18%, driver time per delivery +22 seconds.
Learning: Scope to high-value orders to limit driver time cost.

## EXP-035 Live Tracking Nudges
keywords: live tracking; driver tracking; tracking notification; push notification; where is my order; tracking nudge
status: concluded - shipped
Hypothesis: Push notifications with live driver tracking reduce where-is-my-order contacts.
Result: Contact Rate -7%, Delivery CSAT +0.2. Fatigue and opt-outs appeared after the third push per order.
Learning: Cap pushes at two per order.

## EXP-040 Pickup Wait Compensation
keywords: wait time; pickup wait; wait pay; wait compensation
status: concluded - not shipped
Hypothesis: Paying for pickup wait time improves acceptance at slow stores.
Result: Driver Acceptance Rate +2 pts, Cost Per Delivery +$0.18, no OTD change.
Learning: ROI too low; fix pickup readiness instead.
