"""Reference data drawn from OMB M-25-21 and OMB's Guidance on 2025 Agency AI Reporting.

The wording here is a *summary*. Always check the source memorandum and your
agency's own AI policy before relying on it.
"""

from __future__ import annotations

SOURCES = {
    "M-25-21": "OMB Memorandum M-25-21, Accelerating Federal Use of AI through Innovation, Governance, "
               "and Public Trust (Apr. 3, 2025)",
    "2025-guidance": "OMB, Guidance on 2025 Agency Artificial Intelligence Reporting "
                     "(github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory)",
}

#: High-impact definition (M-25-21 §5): AI whose output serves as a principal
#: basis for decisions or actions with a legal, material, binding, or
#: significant effect on one of these areas.
EFFECT_AREAS = {
    "civil_rights": "Civil rights, civil liberties, or privacy",
    "access_programs": "Access to education, housing, insurance, credit, employment, and other programs",
    "government_services": "Access to critical government resources or services",
    "health_safety": "Human health and safety",
    "critical_infrastructure": "Critical infrastructure or public safety",
    "strategic_assets": "Strategic assets or resources, including high-value property and sensitive or classified information",
}

#: Purposes presumed to be high-impact (M-25-21 §6). ``keywords`` drive the
#: *advisory* text screen; the human-selected list is authoritative.
PRESUMED_CATEGORIES: dict[str, dict] = {
    "safety_critical_infrastructure": {
        "label": "Safety-critical functions of critical infrastructure, government facilities, emergency services, fire and life safety, food safety, or transit control",
        "keywords": ["critical infrastructure", "power grid", "dam", "water treatment", "emergency dispatch",
                     "911", "fire alarm", "life safety", "food safety", "air traffic", "transit control"],
    },
    "physical_movement": {
        "label": "Physically moving robots, vehicles, craft, or industrial equipment that could seriously injure people",
        "keywords": ["autonomous vehicle", "self-driving", "robot", "drone", "unmanned", "industrial machinery"],
    },
    "attack_or_defense": {
        "label": "Kinetic or non-kinetic attack or active-defense measures that could seriously injure people",
        "keywords": ["weapon", "targeting", "active defense", "counter-drone"],
    },
    "hazardous_materials": {
        "label": "Transporting, designing, developing, or using hazardous chemicals or biological agents",
        "keywords": ["hazardous chemical", "biological agent", "pathogen", "toxin", "hazmat"],
    },
    "safety_critical_design": {
        "label": "Designing, building, or testing systems or public infrastructure whose failure would be a significant safety risk",
        "keywords": ["bridge inspection", "structural", "safety certification", "aircraft certification"],
    },
    "healthcare": {
        "label": "Healthcare: medical-device functions, diagnosis, risk assessment, treatment, allocation of public-insurance care, health-insurance costs or underwriting",
        "keywords": ["diagnos", "patient", "clinical", "treatment", "medical device", "triage", "medicare",
                     "medicaid", "underwriting", "suicide risk", "readmission"],
    },
    "facility_access": {
        "label": "Controlling access to, or the security of, government facilities",
        "keywords": ["facility access", "badge", "building security", "entry control"],
    },
    "sanctions_trade": {
        "label": "Adjudicating or enforcing sanctions, trade restrictions, or export, investment, or shipping controls",
        "keywords": ["sanction", "export control", "trade restriction", "tariff", "customs", "shipping control"],
    },
    "protected_speech": {
        "label": "Blocking, removing, hiding, or limiting the reach of protected speech",
        "keywords": ["content moderation", "remove posts", "takedown", "misinformation", "censor"],
    },
    "law_enforcement": {
        "label": "Law enforcement: individual risk assessments, suspect identification, crime forecasting, biometric identification, surveillance, or sentencing, parole, bail, or detention decisions",
        "keywords": ["law enforcement", "suspect", "crime forecast", "predictive policing", "surveillance",
                     "facial recognition", "parole", "bail", "sentencing", "recidivism", "investigation lead"],
    },
    "immigration": {
        "label": "Risk assessments of foreign nationals seeking access to the U.S. (immigration, asylum, detention, travel approval)",
        "keywords": ["immigration", "asylum", "visa", "refugee", "border", "travel authorization", "deportation"],
    },
    "biometric_public": {
        "label": "One-to-many biometric identification in publicly accessible spaces",
        "keywords": ["one-to-many", "face matching", "crowd", "biometric identification"],
    },
    "benefits": {
        "label": "Applying for or adjudicating critical federal services and benefits, continued eligibility, biometric access to benefits, fraud detection, or benefit penalties",
        "keywords": ["benefit", "eligibility", "claims adjudication", "fraud detection", "improper payment",
                     "disability claim", "overpayment", "entitlement"],
    },
    "employment": {
        "label": "Terms or conditions of federal employment: pre-employment screening, hiring, pay, promotion, performance management, discipline, or termination",
        "keywords": ["resume screening", "hiring", "applicant ranking", "promotion", "performance rating",
                     "termination", "disciplinary", "pay setting"],
    },
    "binding_translation": {
        "label": "Language translation whose output is legally binding or directly informs an agency decision",
        "keywords": ["translation", "interpret", "transcription of interviews"],
    },
}

#: The seven minimum risk-management practices for high-impact AI
#: (M-25-21 appendix §4(b)), mapped to the 2025 inventory columns.
PRACTICES: dict[str, dict] = {
    "pre_deployment_testing": {
        "label": "Pre-deployment testing and risk mitigation planning", "ref": "§4(b)(i)",
        "inventory_field": "hi_testing_conducted", "done": {"Yes"},
    },
    "impact_assessment": {
        "label": "AI impact assessment (incl. independent review and documented potential impacts)", "ref": "§4(b)(ii)",
        "inventory_field": "hi_assessment_completed", "done": {"Yes"},
    },
    "independent_review": {
        "label": "↳ Independent review (part of the impact assessment)", "ref": "§4(b)(ii)",
        "inventory_field": "hi_independent_review",
        "done": {"Yes - other office", "Yes - oversight board", "Yes - CAIO"},
    },
    "ongoing_monitoring": {
        "label": "Ongoing monitoring of performance and adverse impacts", "ref": "§4(b)(iii)",
        "inventory_field": "hi_ongoing_monitoring", "done": {"Yes"},
    },
    "operator_training": {
        "label": "Sufficient and periodic training of AI operators", "ref": "§4(b)(iv)",
        "inventory_field": "hi_training_established", "done": {"Yes"},
    },
    "failsafe": {
        "label": "Human oversight, intervention and accountability, with a fail-safe", "ref": "§4(b)(v)",
        "inventory_field": "hi_failsafe_presence", "done": {"Yes", "Not applicable"},
    },
    "appeal_process": {
        "label": "Timely human review and appeal for affected individuals", "ref": "§4(b)(vi)",
        "inventory_field": "hi_appeal_process", "done": {"Yes", "Not applicable", "Precluded by law"},
    },
    "public_feedback": {
        "label": "Consult and incorporate feedback from end users and the public", "ref": "§4(b)(vii)",
        "inventory_field": "hi_public_consultation",
        "done": {"Direct usability testing", "General solicitations of feedback", "Public hearings or meetings", "Other"},
    },
}

PRACTICE_STATUSES = {"Yes", "In-progress", "Waived", "No", "Not applicable", "Precluded by law",
                     "Yes - other office", "Yes - oversight board", "Yes - CAIO",
                     "Direct usability testing", "General solicitations of feedback",
                     "Public hearings or meetings", "Other"}

#: Valid selections from the 2025 inventory data dictionary (short forms).
DEVELOPMENT_STAGES = ["Pre-deployment", "Pilot", "Deployed", "Retired"]
TOPIC_AREAS = ["Administrative Functions", "Cybersecurity", "Emergency Management", "Energy and the Environment",
               "Government Benefits Processing", "Health and Medical", "Human Resources", "Information Technology",
               "International Affairs", "Law Enforcement", "Other", "Procurement and Financial Management",
               "Science", "Service Delivery", "Transportation"]
CLASSIFICATIONS = ["Agentic AI", "Classical/Predictive Machine Learning", "Computer Vision", "Generative AI",
                   "Natural Language Processing", "Reinforcement Learning"]
CONTRACTING = ["Vendor Purchased", "In-house Development", "Contracting and In House"]
