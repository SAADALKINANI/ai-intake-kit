# 2. Is it high-impact? (OMB M-25-21 §5–6)

## The test

AI is **high-impact** when its output serves as a **principal basis** for decisions or actions with a **legal, material, binding, or significant effect** on:

1. civil rights, civil liberties, or privacy;
2. access to education, housing, insurance, credit, employment and other programs;
3. access to critical government resources or services;
4. human health and safety;
5. critical infrastructure or public safety;
6. strategic assets or resources, including high-value property and sensitive or classified information.

Ask two questions in order:

1. **Effect:** could the decision this AI informs significantly affect one of those areas?
2. **Principal basis:** does the AI output actually drive that decision? Or is it one minor input that a person independently weighs?

## Purposes presumed to be high-impact

M-25-21 lists purposes that are presumed high-impact. The list is not exhaustive. Run `aiintake categories` for the keys used in the intake form.

| Key | Purpose |
|---|---|
| `safety_critical_infrastructure` | Safety-critical functions of critical infrastructure, government facilities, emergency services, fire and life safety, food safety, transit control |
| `physical_movement` | Physically moving robots, vehicles or industrial equipment that could seriously injure people |
| `attack_or_defense` | Kinetic or non-kinetic attack or active defense that could seriously injure people |
| `hazardous_materials` | Hazardous chemicals or biological agents |
| `safety_critical_design` | Designing, building or testing systems or infrastructure whose failure would be a significant safety risk |
| `healthcare` | Medical devices, diagnosis, risk assessment, treatment, public-insurance care allocation, health-insurance costs or underwriting |
| `facility_access` | Access to, or security of, government facilities |
| `sanctions_trade` | Sanctions, trade restrictions, export, investment and shipping controls |
| `protected_speech` | Blocking, removing, hiding or limiting protected speech |
| `law_enforcement` | Individual risk assessments, suspect identification, crime forecasting, biometric ID, surveillance, sentencing, parole, bail, detention |
| `immigration` | Risk assessments of foreign nationals seeking access to the U.S. |
| `biometric_public` | One-to-many biometric identification in public spaces |
| `benefits` | Applications for, and adjudication of, critical federal services and benefits, including eligibility, fraud detection and penalties |
| `employment` | Terms and conditions of federal employment, from screening to termination |
| `binding_translation` | Translation that is legally binding or directly informs an agency decision |

## Rebutting a presumption

A use in a presumed category can still be determined **not** high-impact, for example when the AI only de-duplicates case files and an investigator makes every decision. That determination must be put in writing to the CAIO. The 2025 inventory then records the use as "Presumed high-impact, but determined not high-impact", with a justification. In the intake form, set `principal_basis: false` and fill in `not_high_impact_justification`.

## The keyword screen

`aiintake assess` also scans the free-text fields for terms linked to the presumed categories, such as "eligibility", "facial recognition" or "resume screening". A match is **advisory**. It produces a warning so a human takes a second look, and it never decides anything on its own.

> Source: OMB M-25-21, §5–6 of the appendix. This page is a summary; read the memo itself for the authoritative text.
