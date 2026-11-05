# Decision Readiness Review: H06

**Verdict: BLOCKED: a required policy review is not recorded.**  (mode: `hybrid`)

## High severity

- **POLICY_REVIEW: Privacy review not recorded for GPS/location data**
  - Why: The proposal feeds drivers' GPS location history into an LLM, which triggers the privacy policy. The Reviews section records only ops leadership support, with no Privacy review, DPIA or privacy assessment.
  - Evidence: "Use an LLM to draft performance warnings from each driver's GPS location history and delivery records, for manager approval."
  - Fix: Complete and record a Privacy review (DPIA) covering purpose limitation and retention of driver location data before launch.
  - Sources: `policy-compliance#customer-location-and-personal-data`
- **POLICY_REVIEW: Responsible AI review not recorded for LLM use on driver data**
  - Why: An LLM is used on driver data to draft disciplinary warnings. This requires a Responsible AI review covering approved models, data handling and human oversight, and none is recorded. Ops leadership support is not that review.
  - Evidence: "Ops leadership supports the pilot."
  - Fix: Obtain and document a Responsible AI review, including approved model, data handling and the manager-approval oversight design, before the pilot.
  - Sources: `policy-compliance#generative-ai-with-company-data`

---
Advisory pre-review only. It is not an approval and does not replace Legal, Privacy, Compliance, or Data Science review. All sources are synthetic in this prototype.
