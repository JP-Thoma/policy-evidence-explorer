# Policy Evidence Explorer

Exploring research findings across projects to support evidence-informed policy work.

> **Illustrative proof of concept using synthetic research data. Not an official European Commission service.**

The prototype illustrates how user requirements can be translated into a practical, source-traceable evidence exploration service. It is a starting point for user validation, not a production-ready AI system.

## 1. Business context

The Directorate-General for Research and Innovation (DG RTD), through its Common Knowledge and Data Management Service, supports Feedback to Policy (F2P) services. These help channel evidence from EU-funded research projects and other sources into policy development and research programming.

Research findings are spread across many projects, reports, publications and datasets in different formats. Finding, comparing and verifying what several projects say about a topic therefore takes considerable effort.

## 2. Illustrative user need

> A DG RTD policy officer preparing an evidence-based policy briefing needs to understand what EU-funded research projects collectively reveal about a particular policy topic. The officer needs to identify, compare and verify relevant project findings efficiently while retaining responsibility for policy interpretation and writing.

This scenario is an **assumption** used to make the concept concrete. It has not been confirmed with Commission users.

## 3. Intended users

- **Primary:** policy officers preparing briefings or policy input.
- **Secondary:** F2P coordinators, data and AI service teams, data owners and governance stakeholders.

Stakeholder roles are proposed and would need validation (see [docs/user-needs.md](docs/user-needs.md)).

## 4. Proposed service concept

A curated, structured collection of research findings, each linked to its project and source, which a policy officer can filter by topic and theme, compare across projects and trace back to the source document.

```
Policy question -> Identification of relevant sources -> Evidence extraction and organisation
  -> Thematic comparison -> Evidence overview -> Policy officer review
```

The prototype demonstrates thematic comparison and the evidence overview on a curated dataset. Source identification and extraction are assumed. See [docs/concept-and-validation.md](docs/concept-and-validation.md).

## 5. Scope and non-goals

**In scope:** exploring, filtering, comparing and tracing findings on two illustrative topics (urban climate adaptation and sustainable urban mobility).

**Non-goals:**
- drafting policy text or recommending policy options;
- judging the scientific quality of evidence automatically;
- extracting findings from raw reports (the prototype starts from curated data);
- AI, chat interfaces, authentication or production hosting.

## 6. Application features

| Feature | Requirement(s) |
|---|---|
| Policy topic selection (options read from the data) | BR-01 |
| Filters for theme, project, evidence type and keyword, with reset | FR-01, FR-02 |
| Evidence overview counts for the current filtered selection | BR-02 |
| Findings grouped by theme, each with project, topic, theme, evidence type, caveats and source | FR-03, FR-04, FR-05, FR-06 |
| Side-by-side comparison of findings on a theme and a theme-by-project coverage matrix | FR-03 |
| Source reference table; untraceable records are excluded and reported | FR-04, DR-01, DR-02 |
| CSV export of the filtered findings | FR-07 |
| Evidence limitations and description of the human review step | BR-02, FR-05 |

The visual style follows common public-sector design conventions (institutional blue with a yellow accent, Arial typography, flat panels). It deliberately uses no official logos, emblems or Commission branding.

The full provisional catalogue, including requirements **not** implemented in the prototype, is in [requirements/requirements.csv](requirements/requirements.csv).

## 7. Data and provenance

All data is **synthetic**: 14 fictional projects and 34 fictional findings across two policy topics in [data/](data/). Identifiers start with `SYN-`, source references are placeholders (`SYN-SRC-...`) and no URLs are included. Findings are worded as hypothetical results and must not be cited as evidence. They deliberately include different evidence types and some tensions between projects to show why cross-project comparison is useful. See [data/README.md](data/README.md).

A production service would need real, verified sources with document-level references and working links.

## 8. Repository structure

```
policy-evidence-explorer/
├── README.md
├── app.py                      Streamlit application
├── data_utils.py               Data loading, validation and filtering
├── requirements.txt            Python dependencies
├── pytest.ini                  Test configuration
├── .gitignore
├── .streamlit/config.toml      Colour theme and typography
├── data/
│   ├── README.md               Data provenance note
│   ├── projects.csv
│   └── findings.csv
├── requirements/
│   └── requirements.csv        Provisional requirements catalogue
├── docs/
│   ├── user-needs.md           Stakeholders and elicitation approach
│   ├── concept-and-validation.md
│   └── implementation-and-risks.md
└── tests/
    ├── test_data.py            Data, filtering and catalogue tests
    └── test_app.py             Application smoke tests
```

## 9. Installation and execution

Requires Python 3.11 or later. No internet connection or API key is needed at runtime.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application (opens in your browser at http://localhost:8501)
streamlit run app.py

# 4. Run the tests
pytest
```

On Windows, if `python` is not recognised, use `py -m venv .venv` instead.

## 10. Relationship to the practical assignment

The assignment primarily assesses Business Analysis capabilities. The repository is organised accordingly:

| Capability | Where it is shown |
|---|---|
| Stakeholders and user needs | [docs/user-needs.md](docs/user-needs.md) |
| Structuring an ambiguous problem | Known facts, assumptions and open questions in [docs/user-needs.md](docs/user-needs.md) |
| Gathering and translating requirements | Elicitation questions and [requirements/requirements.csv](requirements/requirements.csv) |
| Conceptual service design | [docs/concept-and-validation.md](docs/concept-and-validation.md) |
| Data/AI methods and risks | [docs/implementation-and-risks.md](docs/implementation-and-risks.md) |
| Pilot and implementation planning | [docs/implementation-and-risks.md](docs/implementation-and-risks.md) |
| Technical tool familiarity | The prototype, data model and tests |

## 11. Limitations

- All data is synthetic; nothing in the application is a real research result.
- Two illustrative policy topics only.
- Findings are curated manually; no extraction from source documents.
- Source references are placeholders and cannot be verified.
- No user research has taken place; all requirements are provisional.
- No authentication, access control or production hosting.
- No AI is used. Keyword search is simple text matching.

## 12. Proposed next steps

1. Validate the problem, users and provisional requirements with policy officers and F2P coordinators.
2. Assess data availability, access conditions and curation effort for one real pilot topic.
3. Curate a small real dataset with verified references and repeat prototype-based user testing.
4. Agree a metadata schema and controlled vocabulary with data owners.
5. Only then evaluate whether AI-assisted retrieval or classification would add value, using the curated data as a benchmark.
