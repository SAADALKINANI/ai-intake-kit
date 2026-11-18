# 4. Reporting to the AI use case inventory

Agencies inventory their AI use cases every year and publish the releasable ones. OMB consolidates them on GitHub: see the [2024](https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory) and [2025](https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory) repositories. The 2025 guidance splits reporting into **individually reported use cases** and **consolidated reporting for widely used commercial AI products**.

## Field crosswalk

The intake form in this repo uses the 2025 field names wherever it can, so `aiintake export` produces rows that line up with the consolidated CSV:

| Intake field | Inventory column |
|---|---|
| `use_case_name`, `agency`, `bureau`, `contact_email` | same names (`bureau` → `agency_bureau`) |
| `development_stage` | `development_stage` (Pre-deployment / Pilot / Deployed / Retired) |
| `topic_area`, `classification` | same |
| `problem_solved`, `benefits`, `system_outputs` | same |
| `contracting_usage`, `vendor_name` | same |
| `have_ato`, `system_name_ato` | same |
| `data.description`, `data.has_pii`, `data.pia_url`, `data.demographic_features` | `data_description`, `has_pii`, `pia_url`, `demographic_features` |
| determination | `is_high_impact`, `HI_justification` |
| `practices.*` | `hi_*` columns |

## Quality tips from the 2024 and 2025 data

The [fed-ai-inventory-explorer](https://github.com/SAADALKINANI/fed-ai-inventory-explorer) project analyzes the published inventories. Common problems in the published data include:

- **Missing topic areas.** About 17% of 2025 rows have no topic. Pick the closest one, and avoid "Other" where you can.
- **Vague outputs.** "Insights" tells a reader nothing. Write what the system actually produces, such as "a 0–100 risk score per claim" or "draft response letters".
- **Stage drift.** Use cases that have been "Pre-deployment" for several years should be re-checked or retired.
- **Practice answers that contradict the determination.** For example, a use case marked "Not high-impact" with high-impact practice fields filled in. `aiintake export` only fills the `hi_*` columns for high-impact uses.
