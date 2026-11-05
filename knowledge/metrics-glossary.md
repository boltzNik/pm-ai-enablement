---
id: metrics-glossary
type: metric
owner: SYNTHETIC - LMD Analytics (placeholder owner)
last_reviewed: 2026-09-15
sensitivity: synthetic-demo
---
# LMD Canonical Metrics Glossary (SYNTHETIC)

> All content in /knowledge is invented for this prototype. It mimics the *shape* of enterprise context, not real Walmart data or definitions.

## On-Time Delivery Rate
name: On-Time Delivery Rate
aliases: OTD; on-time delivery; on time delivery; on-time rate
Definition: Share of delivered orders that arrive inside the promised delivery window. Denominator: delivered orders. Excludes customer-rescheduled orders.

## Delivery Defect Rate
name: Delivery Defect Rate
aliases: DDR; defect rate; delivery defects
Definition: Share of delivered orders with at least one defect: missing item, damaged item, wrong address, or arrival more than 30 minutes after the window.

## Cost Per Delivery
name: Cost Per Delivery
aliases: CPD; cost per delivery; delivery cost
Definition: Fully loaded last-mile cost (driver pay, incentives, platform fees, refunds) divided by delivered orders.

## Driver Acceptance Rate
name: Driver Acceptance Rate
aliases: acceptance rate; offer acceptance; driver acceptance
Definition: Share of delivery offers accepted by drivers within the offer window.

## Orders Per Trip
name: Orders Per Trip
aliases: OPT; batching rate; batch rate
Definition: Average number of orders delivered per driver trip. Used to track batching efficiency.

## Driver Hourly Earnings
name: Driver Hourly Earnings
aliases: DHE; driver earnings; hourly earnings
Definition: Net earnings per engaged hour for drivers, including incentives and tips, before vehicle costs.

## Delivery CSAT
name: Delivery CSAT
aliases: CSAT; customer satisfaction; delivery satisfaction
Definition: Average post-delivery customer rating (1-5) on delivery experience only.

## Promise Accuracy
name: Promise Accuracy
aliases: ETA accuracy; eta error; promise accuracy
Definition: Absolute error between promised and actual arrival time, reported as median minutes and P90.

## Contact Rate
name: Contact Rate
aliases: contacts per 100 orders; support contact rate; contact rate
Definition: Customer support contacts per 100 delivered orders attributable to delivery.

## Driver Safety Incident Rate
name: Driver Safety Incident Rate
aliases: DSIR; safety incident rate; driver safety incidents
Definition: Reported driver safety incidents per 10,000 trips.

## Delivery Completion Rate
name: Delivery Completion Rate
aliases: completion rate; delivery completion
Definition: Share of accepted orders that are delivered (not cancelled, failed, or returned to store).

## Deprecated And Ambiguous Terms
name: Deprecated And Ambiguous Terms
deprecated_terms: delivery speed; delivery success; efficiency; customer delight; customer happiness; driver happiness; delivery time; faster handoffs; user engagement
Guidance: These terms are not canonical metrics. Map them to a defined metric: speed or time -> On-Time Delivery Rate or Promise Accuracy; success -> Delivery Completion Rate; happiness or delight -> Delivery CSAT (customers) or Driver Hourly Earnings plus driver retention (drivers); efficiency -> Cost Per Delivery or Orders Per Trip.
