# ai-intake-kit

**Guides and tooling to take a federal AI project from idea to inventory, with the governance checkpoints built in.**

Federal agencies must work out whether each AI use is *high-impact* under OMB M-25-21. High-impact uses need a set of minimum risk-management practices, and every use goes into the annual AI use case inventory. In practice, that information lives in scattered emails and spreadsheets. This kit turns it into one structured intake form. A small Python tool then:

- **validates** the form against the 2025 inventory's valid selections;
- **screens** for high-impact AI, using the six effect areas and the 15 presumed categories, plus an advisory keyword scan of the free text;
- **checks** the seven minimum practices and lists the gaps, including whether a deployed use is non-compliant;
- **renders** a Markdown assessment report for the governance board;
- **exports** rows that line up with the 2025 consolidated inventory CSV.

The project is inspired by GSA's [AI Community of Practice](https://github.com/GSA/The-AI-Community-of-Practice), which shares guidance on doing AI in government. This repo pairs guides like those with a tool that applies them.

## Guides

| | |
|---|---|
| [1. AI project lifecycle](docs/01-ai-project-lifecycle.md) | Stages, checkpoints and artifacts from idea to retirement |
| [2. Is it high-impact?](docs/02-high-impact-determination.md) | The M-25-21 test, the presumed categories and how to rebut one |
| [3. Minimum practices](docs/03-minimum-practices.md) | What "done" looks like for each practice, plus an evidence checklist |
| [4. Inventory reporting](docs/04-inventory-reporting.md) | Field crosswalk and data-quality tips |
| [5. Generative AI checklist](docs/05-generative-ai-checklist.md) | A light-weight checklist for productivity tools |
| Templates | [intake form](docs/templates/intake.yaml) · [impact assessment](docs/templates/impact-assessment.md) · [model card](docs/templates/model-card.md) |

## Tool quick start

```bash
git clone https://github.com/SAADALKINANI/ai-intake-kit.git
cd ai-intake-kit
pip install -e ".[dev]"
pytest

aiintake new my-use-case.yaml               # blank intake form
aiintake assess examples/intakes/*.yaml --out-dir reports/
aiintake export examples/intakes/*.yaml --out inventory.csv
aiintake categories                         # effect areas + presumed purposes
```

The three example intakes show the three typical outcomes:

| Intake | Determination | Result |
|---|---|---|
| [Website FAQ assistant](examples/intakes/01-public-faq-chatbot.yaml) | Not high-impact | Inventory entry only |
| [Benefit claim fraud scoring](examples/intakes/02-benefits-fraud-model.yaml) | **High-impact** (presumed: benefits and fraud detection) | **Not compliant:** monitoring and appeals are in progress, public feedback is missing ([report](examples/reports/02-benefits-fraud-model.md)) |
| [Wildfire smoke detection](examples/intakes/03-wildfire-imagery.yaml) | Not high-impact | Inventory entry only |

```python
from aiintake import assess, to_markdown

a = assess("examples/intakes/02-benefits-fraud-model.yaml")
a.determination      # 'High-impact'
a.practice_status    # {'pre_deployment_testing': 'Done', ..., 'public_feedback': 'Missing'}
print(to_markdown(a))
```

## Sources

- OMB M-25-21, *Accelerating Federal Use of AI through Innovation, Governance, and Public Trust* (April 3, 2025). It replaced M-24-10.
- OMB, *Guidance on 2025 Agency Artificial Intelligence Reporting*, and the 2025 inventory data dictionary in [ombegov/2025-Federal-Agency-AI-Use-Case-Inventory](https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory).

**Disclaimer:** this kit is decision support, not legal advice or an official determination. Policy changes, so check the current memoranda and your agency's own AI policy and CAIO guidance.

## License

Apache 2.0
