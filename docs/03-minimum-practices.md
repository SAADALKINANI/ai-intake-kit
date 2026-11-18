# 3. Minimum risk-management practices for high-impact AI

M-25-21 (appendix §4(b)) sets a floor of practices that every high-impact use must have before and during deployment. The 2025 inventory asks agencies to report the status of each practice, so it is worth tracking them in exactly those terms.

| # | Practice | What "done" looks like | 2025 inventory field |
|---|---|---|---|
| i | **Pre-deployment testing** | Tested in conditions that mirror real use, with a risk mitigation plan for what testing found | `hi_testing_conducted` |
| ii | **AI impact assessment** | Documented intended purpose, expected benefits, data quality, foreseeable impacts on privacy, civil rights and civil liberties, cost, **independent review**, and a signed acceptance of residual risk | `hi_assessment_completed`, `hi_independent_review`, `hi_potential_impacts` |
| iii | **Ongoing monitoring** | Performance, security and adverse-impact monitoring, with periodic human review | `hi_ongoing_monitoring` |
| iv | **Operator training** | Operators can interpret outputs, know the failure modes, and are reassessed periodically | `hi_training_established` |
| v | **Human oversight and fail-safe** | A named accountable official, the ability to intervene or override, and a fail-safe that minimizes significant harm | `hi_failsafe_presence` |
| vi | **Remedies and appeals** | Affected individuals can get timely human review and appeal, where appropriate | `hi_appeal_process` |
| vii | **Public and end-user feedback** | Usability testing, comment solicitations or hearings that actually inform decisions | `hi_public_consultation` |

## Timing, pilots and waivers

- Agencies had 365 days from the memo (April 2025) to document these practices for existing high-impact uses. A high-impact use that is not compliant must be **safely discontinued** until it is.
- **Pilots** can be exempt if they are limited in scale and duration, certified by the CAIO, and offer opt-out where possible. The practices should still be applied where practicable.
- **Waivers** can only be granted by the CAIO, in writing, based on a system-specific risk assessment. They must be reported to OMB and re-certified annually.

## Evidence checklist

Keep these artifacts together, ideally linked from the intake form:

- [ ] Test plan and results, broken down by relevant subgroups
- [ ] Risk mitigation plan
- [ ] Impact assessment, signed, with the independent reviewer named
- [ ] Monitoring plan: metrics, thresholds, who gets alerted, and review cadence
- [ ] Operator training materials and completion records
- [ ] Override and fail-safe procedure
- [ ] Appeal procedure and the notice given to affected individuals
- [ ] Record of public or end-user consultation and what changed as a result

> Source: OMB M-25-21 appendix §4; OMB Guidance on 2025 Agency AI Reporting (data dictionary). Summary only. Consult the source documents.
