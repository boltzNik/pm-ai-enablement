---
id: policy-compliance
type: policy
owner: SYNTHETIC - Enterprise Policy Office (placeholder owner)
last_reviewed: 2026-07-10
sensitivity: synthetic-demo
---
# Policy And Compliance Triggers (SYNTHETIC)

A proposal touching the areas below needs the named review recorded in the document (with a ticket or approval reference) BEFORE build starts.

## Driver Compensation And Classification
trigger_terms: driver pay; pay rate; incentive; incentives; bonus; surge; payout; minimum earnings; classification; contractor
required_review: Legal and Compensation review
review_markers: legal review; compensation review; comp review
Rationale: Pay design affects contractor classification risk and pay-transparency obligations.

## Customer Location And Personal Data
trigger_terms: precise location; gps; geolocation; phone number; home address; personal data; pii; location history
required_review: Privacy review
review_markers: privacy review; dpia; privacy assessment
Rationale: Precise location and contact details are personal data. Purpose limitation and retention must be reviewed.

## Age-Restricted Items
trigger_terms: alcohol; age-restricted; age verification; id check; tobacco
required_review: Compliance review
review_markers: compliance review
Rationale: Age verification at handoff is a legal requirement and cannot be relaxed by product choice.

## Generative AI With Company Data
trigger_terms: llm; generative ai; genai; gpt; ai model; chatbot
required_review: Responsible AI review
review_markers: responsible ai review; rai review; ai governance review
Rationale: Using models on customer, driver, or confidential data requires approved models, data handling, and human oversight design.
