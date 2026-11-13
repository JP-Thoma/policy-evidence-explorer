# Presentation alignment

**Purpose:** a one-page reference to make sure the five-slide presentation and this repository tell the same story. It is not a substitute for the slides.

- **Slide header:** RTD.H5 - Common Knowledge & Data Management Service | Policy Evidence Explorer
- **Slide footer:** Jan Phillip Thoma | November 2026 · Selection Business Analyst: EC/2026/RTD/521000
- No official Commission logos; no suggestion of institutional authorship.

| Slide | Central argument | Supporting repository evidence | Requirement IDs / data identifiers | Critical assumptions and caveats |
|---|---|---|---|---|
| **1. Business need** | A policy officer preparing a briefing may need to compare relevant findings across EU-funded research projects. | README "At a glance"; [user-needs.md §1](user-needs.md#1-known-assumed-and-to-be-validated) (known / assumed / to validate). | BR-01, BR-02 | Working hypothesis; no users interviewed; no quantified pain points or benefits. |
| **2. Requirements elicitation** | Structured engagement with users and stakeholders turns the initial request into prioritised, testable requirements. | [user-needs.md §2-6](user-needs.md#3-elicitation-plan-activities-and-their-outputs): stakeholders, five activities and their outputs, decision-record template, revision history; [requirements.csv](../requirements/requirements.csv). | 16 requirements: BR-01-02, FR-01-09, DR-01-03, NFR-01-02 | All requirements and MoSCoW priorities are provisional author proposals; none validated. |
| **3. Service concept** | A structured evidence workflow lets findings from several projects be explored, compared and traced to their source metadata. | [concept-and-validation.md §2-6](concept-and-validation.md#3-conceptual-workflow); README walkthrough; the prototype. | FR-08 topic selection, FR-02 filtering, FR-03 thematic comparison, FR-04 source references, FR-05 caveats, FR-07 export. **Synthetic example:** SYN-P01 / SYN-F001 (SYN-SRC-P01-01); SYN-P04 / SYN-F010 (SYN-SRC-P04-01); SYN-P04 / SYN-F011 (SYN-SRC-P04-02) | All data synthetic. Source references show a provenance structure; they cannot be verified against real documents. Steps 2-3 of the workflow (source identification, extraction) are not demonstrated. |
| **4. Data and AI** | Conventional data methods support the first iteration. AI may be evaluated later, depending on user needs, data readiness and risks. | [implementation-and-risks.md §4-5](implementation-and-risks.md#4-data-readiness-for-a-real-data-pilot-fair-oriented): FAIR-oriented readiness checklist; AI capability assessment. | DR-01, DR-02, DR-03; FR-09 (future AI, *Won't for this pilot*) | The prototype is a conventional structured-data application, not AI-powered. It is not FAIR-compliant; FAIR is used as a pilot checklist. |
| **5. Implementation** | A bounded real-data pilot tests evidence quality, feasibility, usefulness and adoption before wider implementation. | [implementation-and-risks.md §1-3, 7, 9](implementation-and-risks.md#1-implementation-sequence); [concept-and-validation.md §7](concept-and-validation.md#7-pilot-evaluation-framework) (evaluation framework, GO / REVISE / STOP). | DR-03, NFR-01, NFR-02 | Pilot = **one policy topic with several themes** (the prototype has two synthetic topics). No success thresholds agreed; roles to be confirmed with RTD.H5. |

**Terms to use consistently:** policy officer (primary user); F2P; RTD.H5; reported finding; source reference; evidence type; caveat; thematic comparison; structured evidence overview; prototype (synthetic data) versus real-data pilot; GO / REVISE / STOP.

**Avoid:** "AI-powered", "validated requirements", "verified sources", "user research shows", or any efficiency figures.
