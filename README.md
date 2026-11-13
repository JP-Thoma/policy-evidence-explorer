# Policy Evidence Explorer

**Live demo:** [policy-evidence-explorer.streamlit.app](https://policy-evidence-explorer.streamlit.app) (synthetic data; may take about 30 seconds to start)

A Business Analysis case study, with a small working prototype, on how findings from several EU-funded research projects could be explored, compared and traced to their sources for evidence-informed policy work.

> **Independent, illustrative proof of concept** prepared by Jan Phillip Thoma for the practical assignment of selection procedure EC/2026/RTD/521000 (Business Analyst – Feedback to Policy Data and AI Services, RTD.H5). It is not a European Commission service, and all research projects and findings in it are **synthetic**.

## At a glance

**The assumed business challenge.** Evidence from EU-funded research is spread across many projects, reports, publications and datasets. Feedback to Policy (F2P) aims to make it usable in policy development, but bringing together what several projects say about one topic takes time and expertise.

**The policy officer's task.** The illustrative user is a policy officer preparing a briefing, who needs to find relevant findings, compare them across projects, understand their limitations and check the sources, while keeping full responsibility for interpretation and drafting.

**The proposed service.** A curated collection of research findings, each linked to its project and source and carrying its evidence type and caveats. The officer selects a topic, compares findings by theme across projects and takes the result into their own review. The service generates no conclusions or policy recommendations.

**What the prototype demonstrates.** Topic selection, filtering, side-by-side comparison by theme, visible caveats, a source reference on every finding, and export, using 14 synthetic projects and 34 synthetic findings.

**What would need to be validated.** Whether the need is real and important; what users actually require; whether a reliable evidence base can be curated from real project outputs with acceptable effort; and whether the result fits existing work. No users have been interviewed and no requirement has been validated.

## Demonstration: comparing evidence on urban heat

This walkthrough uses the prototype's synthetic data and can be followed without running the application.

1. **Select the topic** *Urban climate adaptation* (8 projects, 19 findings, 4 themes).
2. **Filter by theme** in the sidebar: *Urban heat mitigation*. The overview updates to 6 findings from 4 projects.
3. **Filter by project:** *Synthetic Project 01 - Street trees and pedestrian thermal comfort* and *Synthetic Project 04 - Cool surfaces and reflective materials*. The overview shows 2 projects and 4 findings.
4. **Compare findings.** In the *Compare findings* tab, the *Urban heat mitigation* section shows both projects side by side. Three of the four findings illustrate the point:

| Finding (synthetic) | What it concerns | Evidence type | Stated caveat | Source reference |
|---|---|---|---|---|
| SYN-F001 – Street tree canopy associated with lower perceived heat stress (SYN-P01) | Surface temperature and perceived heat stress at pedestrian level | Field measurement study | Two neighbourhoods, one summer season | SYN-SRC-P01-01 |
| SYN-F010 – Reflective pavements lower surface temperatures (SYN-P04) | Road surface temperature | Field measurement study | Surface temperature only; pedestrian thermal comfort not measured | SYN-SRC-P04-01 |
| SYN-F011 – Reflected radiation may increase pedestrian heat exposure (SYN-P04) | Radiation reaching pedestrians | Modelling or simulation | Model-based; in tension with surface measurements; needs field validation | SYN-SRC-P04-02 |

5. **Export for review.** The *Table and export* tab lists the four findings with their finding IDs and source references; *Download filtered findings (CSV)* exports exactly this selection.

**What the comparison shows.** A lower surface temperature (SYN-F010) does not necessarily mean better conditions for people on the street (SYN-F011), and the street-tree study (SYN-F001) measured a different outcome under different conditions. Placing outcome, method and caveat side by side makes these differences visible. Deciding what they mean for a briefing remains the officer's job.

**Why this matters from a Business Analysis perspective.** The walkthrough turns requirements into an observable task: select a topic (FR-08), narrow it (FR-02), compare across projects (FR-03), see caveats (FR-05) and sources (FR-04), and export (FR-07). Real users could perform this task during elicitation and say what is missing; that is the prototype's main purpose.

## Business Analysis approach

- **Assumptions made explicit.** [docs/user-needs.md](docs/user-needs.md) separates what is known, what is assumed and what must be validated.
- **Stakeholders and elicitation.** Five proposed activities, each linked to a specific output such as a process map, a time baseline or agreed acceptance criteria.
- **Requirements.** [requirements/requirements.csv](requirements/requirements.csv) holds 16 provisional requirements, each linking a user need to a testable acceptance criterion, a MoSCoW priority and an honest statement of prototype coverage.
- **Validation and change.** Priorities are the author's proposals. The user-needs document explains how stakeholder decisions, conflicts and changes would be recorded.

## Proposed service and prototype boundaries

```
Policy question -> Relevant research sources -> Evidence extraction and organisation
  -> Thematic comparison -> Structured evidence overview -> Policy officer review
```

The prototype starts from an already structured synthetic dataset. It **demonstrates** topic selection, filtering, thematic comparison and the evidence overview. It does **not** discover documents, extract findings from reports, verify real sources, assess scientific quality, generate AI summaries or support a review workflow.

The documentation distinguishes four levels: the **service concept**, this **prototype**, a proposed **real-data pilot**, and possible **later AI enhancements**. See [docs/concept-and-validation.md](docs/concept-and-validation.md).

## Data, evidence quality and AI

- **Synthetic data.** All projects, findings, documents and references are fictional (`SYN-` identifiers, no URLs) and must not be cited. See [data/README.md](data/README.md).
- **Source references.** Each finding carries a project ID, document title and reference (`SYN-SRC-...`). This shows a provenance structure; it does not allow verification against real documents.
- **Evidence limitations.** Evidence type and caveats appear with every finding; overview counts are labelled as dataset coverage, not strength of evidence.
- **Human review.** Curation, source verification, interpretation and use in a briefing remain human responsibilities.
- **Methods.** Conventional only: structured fields, filtering, keyword search, grouping, cross-tabulation and data checks. No AI.
- **AI later, if justified.** Semantic retrieval, theme classification, candidate extraction and source-grounded synthesis are assessed in [docs/implementation-and-risks.md](docs/implementation-and-risks.md). A reliable data foundation and a verified user need come first.

## From concept to pilot

The proposed first pilot covers **one policy topic with several themes** (the prototype has two topics to show the design is not topic-specific), using expert-curated findings from real project outputs, working source references and a small group of policy users with a defined briefing task.

It would test relevance, fidelity to sources, efficiency against a baseline, usability, curation feasibility and fit with existing work, against thresholds agreed in advance, leading to a **GO / REVISE / STOP** decision. A FAIR-oriented checklist sets out the metadata a real pilot would need.

## Run locally

Requires Python 3.11 or later. No internet connection or API key is needed at runtime.

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows PowerShell
source .venv/bin/activate        # macOS / Linux
pip install -r requirements.txt
streamlit run app.py             # opens http://localhost:8501
pytest                           # runs the automated tests
```

On Windows, use `py -m venv .venv` if `python` is not recognised.

## Supporting documentation

| Document | Question it answers |
|---|---|
| [docs/user-needs.md](docs/user-needs.md) | Who are the stakeholders, and how would needs be elicited and validated? |
| [requirements/requirements.csv](requirements/requirements.csv) | What should the service do, how important is each requirement, and how would it be tested? |
| [docs/concept-and-validation.md](docs/concept-and-validation.md) | What is the service concept, what does the prototype cover, and how would a pilot be evaluated? |
| [docs/implementation-and-risks.md](docs/implementation-and-risks.md) | How would it be implemented, what data is needed, where might AI help, and what are the risks? |
| [docs/presentation-alignment.md](docs/presentation-alignment.md) | How does the repository support the five-slide presentation? |
| [data/README.md](data/README.md) | What is the synthetic dataset and how is it labelled? |
| `app.py`, `data_utils.py`, `tests/` | The Streamlit prototype, its data and filtering logic, and automated tests. |
