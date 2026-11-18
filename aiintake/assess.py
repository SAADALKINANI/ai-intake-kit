"""Validate an intake, screen it for high-impact AI and check the minimum practices."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .policy import (CLASSIFICATIONS, CONTRACTING, DEVELOPMENT_STAGES, EFFECT_AREAS, PRACTICE_STATUSES,
                     PRACTICES, PRESUMED_CATEGORIES, TOPIC_AREAS)

REQUIRED = ["use_case_name", "agency", "bureau", "development_stage", "problem_solved", "benefits",
            "system_outputs"]
REQUIRED_ACTIVE = ["topic_area", "classification", "contracting_usage"]  # pre-deployment, pilot, deployed


@dataclass
class Assessment:
    intake: dict
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    presumed: list[str] = field(default_factory=list)
    suggested: dict[str, list[str]] = field(default_factory=dict)
    determination: str = ""
    rationale: str = ""
    practice_status: dict[str, str] = field(default_factory=dict)
    gaps: list[str] = field(default_factory=list)
    compliance: str = ""
    next_steps: list[str] = field(default_factory=list)

    @property
    def is_high_impact(self) -> bool:
        return self.determination == "High-impact"

    @property
    def ok(self) -> bool:
        return not self.errors


def load_intake(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: intake must be a YAML mapping")
    return data


def _text(intake: dict) -> str:
    parts = [str(intake.get(k, "")) for k in ("use_case_name", "problem_solved", "benefits", "system_outputs")]
    parts.append(str((intake.get("decision_role") or {}).get("description", "")))
    return " ".join(parts).lower()


def validate(intake: dict, a: Assessment) -> None:
    for k in REQUIRED:
        if not str(intake.get(k) or "").strip():
            a.errors.append(f"Missing required field '{k}'")
    stage = intake.get("development_stage")
    if stage and stage not in DEVELOPMENT_STAGES:
        a.errors.append(f"development_stage '{stage}' must be one of {DEVELOPMENT_STAGES}")
    if stage in {"Pre-deployment", "Pilot", "Deployed"}:
        for k in REQUIRED_ACTIVE:
            if not intake.get(k):
                a.errors.append(f"Missing '{k}' (required for {stage} use cases)")
    for key, allowed in (("topic_area", TOPIC_AREAS), ("classification", CLASSIFICATIONS),
                         ("contracting_usage", CONTRACTING)):
        v = intake.get(key)
        if v and v not in allowed:
            a.errors.append(f"{key} '{v}' is not a valid selection. Options: {', '.join(allowed)}")
    email = intake.get("contact_email")
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", str(email), flags=re.I):
        a.errors.append(f"contact_email '{email}' does not look like an email address")
    role = intake.get("decision_role") or {}
    for area in role.get("effect_areas") or []:
        if area not in EFFECT_AREAS:
            a.errors.append(f"Unknown effect area '{area}'. Options: {', '.join(EFFECT_AREAS)}")
    for cat in role.get("presumed_categories") or []:
        if cat not in PRESUMED_CATEGORIES:
            a.errors.append(f"Unknown presumed category '{cat}'. Options: {', '.join(PRESUMED_CATEGORIES)}")
    for p, status in (intake.get("practices") or {}).items():
        if p in ("potential_impacts",):
            continue
        if p not in PRACTICES:
            a.warnings.append(f"Unknown practice '{p}' ignored")
            continue
        values = status if isinstance(status, list) else [status]
        for v in values:
            if v not in PRACTICE_STATUSES:
                a.errors.append(f"practices.{p} has invalid status '{v}'")
    data = intake.get("data") or {}
    if data.get("has_pii") and not data.get("pia_url"):
        a.warnings.append("Uses PII but no privacy impact assessment (pia_url) is listed")
    if intake.get("classification") == "Generative AI" and data.get("has_pii"):
        a.warnings.append("Generative AI with PII: confirm the tool is approved for PII and inputs are not retained by the vendor")
    if intake.get("contracting_usage") in {"Vendor Purchased", "Contracting and In House"} and not intake.get("vendor_name"):
        a.warnings.append("Vendor involved but vendor_name is empty")


def screen(intake: dict, a: Assessment) -> None:
    """High-impact determination (M-25-21 §5-6). Keyword hits are advisory only."""
    role = intake.get("decision_role") or {}
    a.presumed = list(role.get("presumed_categories") or [])
    text = _text(intake)
    for key, cat in PRESUMED_CATEGORIES.items():
        hits = sorted({k for k in cat["keywords"] if k in text})
        if hits and key not in a.presumed:
            a.suggested[key] = hits
    principal = role.get("principal_basis")
    areas = role.get("effect_areas") or []
    if principal is None:
        a.warnings.append("decision_role.principal_basis not answered: is the AI output a principal basis "
                          "for a decision or action?")
    if principal and areas:
        a.determination = "High-impact"
        a.rationale = ("The output is a principal basis for decisions with significant effects on: "
                       + "; ".join(EFFECT_AREAS[x] for x in areas) + ".")
    elif a.presumed and principal is False:
        a.determination = "Presumed high-impact, but determined not high-impact"
        a.rationale = ("The use falls in a presumed high-impact category, but the intake states the output is not a "
                       "principal basis for the decision. This must be documented in a written determination to the "
                       "CAIO, and the justification is reported in the inventory (HI_justification).")
        if not str(role.get("not_high_impact_justification") or "").strip():
            a.errors.append("Presumed high-impact use rebutted without decision_role.not_high_impact_justification")
    elif a.presumed:
        a.determination = "High-impact"
        a.rationale = "The use falls in a category presumed high-impact and the presumption has not been rebutted."
    else:
        a.determination = "Not high-impact"
        a.rationale = "No high-impact effect areas or presumed categories were identified."
    if a.suggested and a.determination == "Not high-impact":
        a.warnings.append("The description mentions terms linked to presumed high-impact categories ("
                          + ", ".join(a.suggested) + "). Confirm with your CAIO office.")


def check_practices(intake: dict, a: Assessment) -> None:
    stage = intake.get("development_stage")
    if not a.is_high_impact:
        a.compliance = "Minimum practices not required (not high-impact)"
        a.next_steps.append("Record the use case in the annual AI use case inventory.")
        return
    pilot = intake.get("pilot_exemption") or {}
    if stage == "Pilot" and all(pilot.get(k) for k in ("certified_by_caio", "limited_scale_and_duration",
                                                         "opt_out_available")):
        a.compliance = "Pilot exemption claimed: practices apply where practicable"
        a.next_steps.append("Keep the CAIO pilot certification on file and plan full compliance before scaling.")
    reported = intake.get("practices") or {}
    for key, spec in PRACTICES.items():
        val = reported.get(key)
        vals = val if isinstance(val, list) else ([val] if val else [])
        if any(v in spec["done"] for v in vals):
            status = "Done"
        elif "Waived" in vals:
            status = "Waived"
        elif "In-progress" in vals:
            status = "In progress"
        else:
            status = "Missing"
        a.practice_status[key] = status
        if status in {"Missing", "In progress"}:
            a.gaps.append(f"{spec['label']} ({spec['ref']}): {status.lower()}")
        if status == "Waived":
            a.next_steps.append(f"Confirm a written CAIO waiver for '{spec['label']}' exists, has been reported "
                                "to OMB, and is re-certified annually.")
    if not str(reported.get("potential_impacts") or "").strip():
        a.gaps.append("Impact assessment does not describe potential impacts on privacy, civil rights and civil liberties")
    if not a.compliance:
        if not a.gaps:
            a.compliance = "All minimum practices documented"
        elif stage == "Deployed":
            a.compliance = ("NOT COMPLIANT: a deployed high-impact use must implement the minimum practices "
                            "(or hold a waiver) or be safely discontinued")
        else:
            a.compliance = "Gaps must be closed before deployment"
    for g in a.gaps:
        a.next_steps.append(f"Close gap: {g}")


def _normalize(intake: dict) -> dict:
    """YAML 1.1 turns bare Yes/No into booleans; map practice answers back to text."""
    practices = dict(intake.get("practices") or {})
    fix = lambda v: {True: "Yes", False: "No"}.get(v, v) if isinstance(v, bool) else v  # noqa: E731
    for k, v in practices.items():
        practices[k] = [fix(x) for x in v] if isinstance(v, list) else fix(v)
    return {**intake, "practices": practices}


def assess(intake: dict | str | Path) -> Assessment:
    if not isinstance(intake, dict):
        intake = load_intake(intake)
    intake = _normalize(intake)
    a = Assessment(intake=intake)
    validate(intake, a)
    screen(intake, a)
    check_practices(intake, a)
    return a
