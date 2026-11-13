# Service concept and validation

**Question this document answers:** what would the service do, what does the prototype actually demonstrate, where do people review the evidence, and how would a real-data pilot be evaluated?

## 1. Objective

Help a policy officer identify, compare and verify what several EU-funded research projects report on a policy topic, so that the evidence can be used in a briefing while the officer keeps full responsibility for interpretation, judgement and drafting.

The service organises **reported findings**. It does not draft policy, recommend or rank policy options, or assess the scientific quality of studies.

## 2. Four levels that must not be confused

| Level | What it is | Status |
|---|---|---|
| **A. Service concept** | The full workflow below, from policy question to officer review, operating on real research outputs. | Proposal; not validated with users. |
| **B. Prototype** (this repository) | A small application that filters, groups, compares and exports findings from a curated **synthetic** dataset. | Built; covered by automated tests. |
| **C. Real-data pilot** | One policy topic with several themes, expert-curated findings from real project outputs, working source references and a small group of users. | Proposed (see [implementation-and-risks.md](implementation-and-risks.md)). |
| **D. Later AI enhancements** | Possible support for retrieval, classification, extraction or synthesis (FR-09). | Not planned before the pilot has been evaluated. |

## 3. Conceptual workflow

```
Policy question
  -> Identification of relevant research sources
  -> Evidence extraction and organisation
  -> Thematic comparison
  -> Structured evidence overview
  -> Policy officer review and interpretation
```

| Step | Service concept | Prototype | Real-data pilot |
|---|---|---|---|
| **1. Policy question** | The officer defines the topic and scope of the briefing. | Selects a predefined topic and optional themes (FR-08, FR-02). No free-text questions. | Same, for one topic. |
| **2. Relevant sources** | Relevant projects, deliverables and publications are identified. | **Not performed.** Starts from a fixed synthetic set of projects. | Done manually by curators, with documented selection criteria (DR-03). |
| **3. Extraction and organisation** | Findings, evidence type, limitations and source references are recorded in a consistent structure. | **Not performed.** Findings are pre-entered in `data/findings.csv`. | Done manually by curators against an agreed schema (DR-02). |
| **4. Thematic comparison** | Findings are grouped by theme and compared across projects. | **Demonstrated.** One foldable section per theme with project panels side by side (FR-03). | Same, with real findings. |
| **5. Evidence overview** | A structured overview with counts, caveats and sources. | **Demonstrated.** Counts, distributions, caveats, synthetic references and CSV export (FR-04, FR-05, FR-07). | Same, with working source links. |
| **6. Officer review** | The officer verifies sources, weighs caveats, consults experts and decides what to use. | **Not supported** by the application; described in this document only. | Supported by user guidance; tested in task sessions. |

Steps 2 and 3 are where most of the real effort, cost and risk lie. They are not demonstrated by the prototype and are therefore the main focus of the pilot.

## 4. What the prototype demonstrates, and what it does not

**Demonstrates:** topic selection; filtering by theme, project, evidence type and keyword; findings with evidence type and caveats; thematic comparison across projects; overview counts labelled as dataset coverage; placeholder source references on every finding; exclusion of records without a project link or source reference; CSV export.

**Does not demonstrate:** discovery of real documents; extraction of findings from reports; verification against genuine sources (synthetic references cannot be resolved); assessment of scientific quality; AI-generated synthesis; a review or sign-off workflow.

## 5. Inputs, processing and outputs

| | Prototype | Pilot (additional) |
|---|---|---|
| **Inputs** | Project records (ID, title, topic, description, research area); finding records (ID, project, title, description, topic, theme, evidence type, limitation, source document, source reference). | Real project outputs; document- or section-level references and links; access conditions; curation metadata (curator, review date, verification status). |
| **Processing** | Exact-match filtering, case-insensitive keyword search, grouping, cross-tabulation, structural data checks. All conventional methods; no AI. | Same, plus controlled vocabularies and a manual curation and sample-verification process. |
| **Outputs** | Filtered findings with caveats and references; dataset counts; comparison by theme; CSV export. | Same, with working source links and published coverage criteria. |

## 6. Human review points

| Review point | What is checked | Likely responsible role (to be agreed) | In prototype? |
|---|---|---|---|
| **Evidence curation** | The recorded finding, evidence type and caveat faithfully reflect the source. | Curator or subject-matter expert | No (synthetic data) |
| **Source verification** | The reference resolves to the cited passage. | Curator (sample check); policy officer before use | No |
| **Caveats and context** | Limitations, setting and method are understood before comparing findings. | Policy officer, with experts where needed | Caveats displayed |
| **Policy interpretation** | What agreements, tensions and gaps mean for the policy question. | Policy officer | No interpretation generated |
| **Use in a briefing** | Whether and how a finding is cited. | Policy officer and line hierarchy | Outside the service |

Who is accountable for the content of the evidence base, who may publish curated findings, and how corrections are handled would need to be agreed with RTD.H5, the policy units and data owners. The roles above are working assumptions, not a description of current Commission practice.

## 7. Pilot evaluation framework

The pilot would answer one question: **is a curated, source-traceable evidence overview useful and feasible enough to justify wider implementation?**

| Dimension | Question | Method | Assessed by | Illustrative indicator (to be agreed) |
|---|---|---|---|---|
| **Relevance** | Can officers find evidence relevant to a representative briefing task? | Task-based sessions with real pilot data | Pilot users; BA observes | Share of tasks where users judge the retrieved findings relevant and sufficient as a starting point |
| **Traceability and fidelity** | Do curated findings match their original documents? | Independent review of a random sample against sources | Second curator or subject-matter expert | Share of sampled findings whose reference resolves and whose wording is judged faithful |
| **Efficiency** | How does time spent finding and checking evidence compare with today? | Baseline from task observation (elicitation activity 3) versus the same task in the pilot | BA, with users | Time per task compared with baseline, with users' own assessment |
| **Usability** | Can users complete the core task without extensive support? | Task-based sessions; short structured questionnaire | BA; users | Completion without facilitator help; recurring usability issues |
| **Data feasibility** | Can a useful dataset be curated with acceptable effort and quality? | Log of curation effort; data quality checks; governance review | Curators; data owners; product owner | Effort per finding; share of sources accessible and reusable |
| **Adoption** | Would the service fit existing work and responsibilities? | Structured feedback; discussion with F2P coordinators and unit management | Product owner; F2P coordinators | Stated willingness to use; an identified service owner |

No targets have been set. Thresholds would be agreed with the business-side product owner **before** the pilot starts, so that results cannot be interpreted selectively afterwards.

### Decision after the pilot

| Decision | Typical conditions |
|---|---|
| **GO** (extend to further topics) | Relevance and fidelity meet agreed thresholds; curation effort is sustainable; a service owner is identified. |
| **REVISE** (adjust and re-test) | Users value the concept, but fidelity, usability or curation effort fall short in ways that can be addressed (e.g. schema, guidance, scope). |
| **STOP** | Users do not find the overview useful for real tasks, or a reliable evidence base cannot be produced with acceptable effort or within access constraints. |

## 8. Dependencies and constraints

- Access to project outputs, including rules for non-public deliverables.
- Capacity of curators or subject-matter experts to extract and check findings.
- Agreement on a metadata schema and controlled vocabularies.
- Fit with existing Commission platforms, tools and data governance rules.
- Availability of policy officers, whose time is limited.
- For any later AI component: approved tools and infrastructure, and evaluation against the curated reference data.
