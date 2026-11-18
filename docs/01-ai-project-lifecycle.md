# 1. The federal AI project lifecycle

This guide walks a program office from idea to retirement. It shows where the governance checkpoints fall and which artifact each checkpoint produces. It summarizes OMB M-25-21 and the 2025 AI use case reporting guidance. Your agency's own AI policy and your Chief AI Officer (CAIO) have the final word.

| Stage | Key questions | Artifacts | Tooling in this repo |
|---|---|---|---|
| **0. Idea** | What problem are we solving? Is AI the right tool, or would a rule or a better form do? | Problem statement, success metric | — |
| **1. Intake** | Who owns it? What data does it need? Is it high-impact? | Intake form | `aiintake new`, `aiintake assess` |
| **2. Acquire / build** | Buy, build or both? Who owns the data rights, model documentation and exit path? | Acquisition plan (see OMB M-25-22), data sharing agreements, PIA if PII is involved | [templates/model-card.md](templates/model-card.md) |
| **3. Test** | Does it work in conditions like real use, for every group it affects? | Test report, risk mitigation plan | [templates/impact-assessment.md](templates/impact-assessment.md) |
| **4. Pilot** | Can we limit the scale, the duration and who is exposed? | CAIO pilot certification if you claim the pilot exemption | intake `pilot_exemption` block |
| **5. Deploy** | Are the minimum practices in place, or waived in writing? | AI impact assessment, ATO, operator training records | `aiintake assess` gap list |
| **6. Operate** | Is performance drifting? Are complaints or appeals rising? | Monitoring dashboards, periodic human review | — |
| **7. Report** | Is the use case in the annual inventory with current answers? | Inventory row | `aiintake export` |
| **8. Retire** | How do we shut it down safely and keep the records? | Decommission plan, records disposition | — |

## Practical tips

- **Write the success metric before you pick the model.** "Reduce average claim processing time from 30 to 20 days" is testable. "Use AI for claims" is not.
- **Start the intake early.** A high-impact determination adds testing, an impact assessment and appeal processes. It is far cheaper to design these in than to retrofit them.
- **Treat vendor AI the same as in-house AI.** The minimum practices apply whether the agency builds the system or buys it. Put documentation and testing access requirements into the contract.
- **Re-assess when the use changes.** A summarization tool becomes high-impact if its summaries start to drive eligibility decisions.
