import csv
from pathlib import Path

import pytest
import yaml

from aiintake import assess, export_inventory, to_markdown
from aiintake.cli import main as cli
from aiintake.policy import PRACTICES, PRESUMED_CATEGORIES

EX = Path(__file__).parent.parent / "examples" / "intakes"


def base(**over):
    d = yaml.safe_load((EX / "01-public-faq-chatbot.yaml").read_text())
    d.update(over)
    return d


def test_reference_data_shape():
    assert len(PRESUMED_CATEGORIES) == 15 and len(PRACTICES) == 8


def test_chatbot_not_high_impact():
    a = assess(EX / "01-public-faq-chatbot.yaml")
    assert a.ok and a.determination == "Not high-impact" and not a.practice_status


def test_fraud_model_high_impact_and_noncompliant():
    a = assess(EX / "02-benefits-fraud-model.yaml")
    assert a.ok and a.is_high_impact
    assert a.practice_status["ongoing_monitoring"] == "In progress"
    assert a.practice_status["public_feedback"] == "Missing"
    assert a.compliance.startswith("NOT COMPLIANT")


def test_imagery_keyword_screen_is_quiet():
    a = assess(EX / "03-wildfire-imagery.yaml")
    assert a.determination == "Not high-impact" and a.ok


def test_keyword_suggestion_warns():
    a = assess(base(problem_solved="Rank applicants during resume screening for hiring managers."))
    assert "employment" in a.suggested and any("presumed high-impact" in w for w in a.warnings)


def test_rebuttal_requires_justification():
    d = base(decision_role={"principal_basis": False, "presumed_categories": ["law_enforcement"]})
    a = assess(d)
    assert a.determination.startswith("Presumed") and any("justification" in e for e in a.errors)
    d["decision_role"]["not_high_impact_justification"] = "Output only de-duplicates case files; analysts decide."
    assert assess(d).ok


def test_validation_errors():
    a = assess(base(development_stage="Live", topic_area="Space", contact_email="nope"))
    joined = " ".join(a.errors)
    assert "development_stage" in joined and "topic_area" in joined and "contact_email" in joined


def test_pilot_exemption():
    d = yaml.safe_load((EX / "02-benefits-fraud-model.yaml").read_text())
    d["development_stage"] = "Pilot"
    d["pilot_exemption"] = {"certified_by_caio": True, "limited_scale_and_duration": True, "opt_out_available": True}
    assert assess(d).compliance.startswith("Pilot exemption")


def test_markdown_and_export(tmp_path):
    a = assess(EX / "02-benefits-fraud-model.yaml")
    md = to_markdown(a)
    assert "High-impact" in md and "§4(b)(iii)" in md
    out = export_inventory([a, assess(EX / "01-public-faq-chatbot.yaml")], tmp_path / "inv.csv")
    rows = list(csv.DictReader(open(out)))
    assert rows[0]["is_high_impact"] == "High-impact" and rows[0]["hi_ongoing_monitoring"] == "In-progress"
    assert rows[1]["hi_testing_conducted"] == ""


def test_cli(tmp_path, capsys):
    form = tmp_path / "new.yaml"
    assert cli(["new", str(form)]) == 0 and form.exists()
    assert cli(["assess", str(form)]) == 2  # blank form has errors
    assert cli(["assess", *map(str, sorted(EX.glob("*.yaml"))), "--out-dir", str(tmp_path / "r")]) == 0
    assert len(list((tmp_path / "r").glob("*.md"))) == 3
    assert cli(["categories"]) == 0
    assert "law_enforcement" in capsys.readouterr().out
