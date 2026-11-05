---
id: experimentation-standards
type: standard
owner: SYNTHETIC - LMD Data Science (placeholder owner)
last_reviewed: 2026-08-20
sensitivity: synthetic-demo
---
# Experimentation Standards (SYNTHETIC)

## Marketplace Interference
applies_to_categories: ETA and delivery promise; Driver pay and incentives; Routing, dispatch and batching
acceptable_designs: switchback; geo; market; cluster; zone-level; store-level
Rule: Drivers, customers and orders share one supply pool, so individual-level randomization leaks effects between arms for changes to pay, routing, or promises. Use switchback, geo, or market-level designs.

## Duration And Seasonality
min_days: 14
Rule: Run at least 14 days (two full weekly cycles) to cover weekday and weekend demand. Shorter tests need Data Science sign-off.

## Pre-Registration
Rule: Before launch record the primary metric, minimum detectable effect (MDE), sample size or power, and stopping rule. No peeking at results to stop early on a win.

## Guardrail Breach Policy
Rule: If any guardrail breaches its stop threshold the test stops and the owner reports to the LMD experimentation board within one business day.
