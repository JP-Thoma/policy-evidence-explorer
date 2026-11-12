# Service concept and validation approach

## 1. Objective and scope

**Objective:** help a policy officer identify, compare and verify what several EU-funded research projects report on a policy topic, so that an evidence-informed briefing can be prepared more efficiently while the officer retains responsibility for interpretation and drafting.

**In scope (concept):** a curated, structured collection of research findings, linked to projects and sources, which can be filtered by topic and theme, compared across projects and traced back to the source document.

**Out of scope:** drafting policy text, recommending or ranking policy options, assessing the scientific quality of individual studies automatically, and replacing expert or policy judgement.

## 2. Conceptual workflow

```
Policy question
  -> Identification of relevant sources
  -> Evidence extraction and organisation
  -> Thematic comparison
  -> Evidence overview
  -> Policy officer review
```

| Step | Description | Represented in the prototype? |
|---|---|---|
| **1. Policy question** | The officer defines the topic and scope of the briefing. | **Partly.** The officer selects a predefined topic and optional themes. Free-text policy questions are not supported. |
| **2. Identification of relevant sources** | Relevant projects, deliverables and publications are identified (e.g. from programme databases and repositories). | **Assumed.** The prototype starts from a small curated set of synthetic projects. Source identification is not performed. |
| **3. Evidence extraction and organisation** | Individual findings, their evidence type and limitations are extracted from sources and recorded in a consistent structure. | **Assumed.** Findings are pre-entered in `data/findings.csv`. The prototype does **not** extract findings from raw project reports. |
| **4. Thematic comparison** | Findings are grouped by theme and compared across projects to show consistencies, tensions and gaps. | **Yes.** Foldable theme sections with project findings side by side, and a theme-by-project coverage overview. |
| **5. Evidence overview** | A structured overview of findings, counts, caveats and sources for the current selection. | **Yes.** Overview counts and distributions, project panels per theme, a table view and CSV export. |
| **6. Policy officer review** | The officer verifies sources, considers caveats, consults experts and decides what to use. | **Described only.** The review step is explained on screen but not supported by a workflow. |

The key distinction is that the prototype demonstrates steps 4 and 5 on a **curated, structured dataset**. Steps 2 and 3 are where most of the real effort and risk lie, and they would be central to a pilot.

## 3. Inputs

- Policy topic and, optionally, themes of interest (from the user).
- Project metadata: identifier, title, topic, description, research area.
- Findings: identifier, project link, title, description, topic, theme, evidence type, limitations, source document, source reference.
- In a real service: document-level references and links, access conditions, curation metadata (who curated, when, review status).

## 4. Analytical tasks

| Task | Method in prototype | Possible method in a pilot |
|---|---|---|
| Filter by topic, theme, project, evidence type | Exact matching on structured fields | Same, with a controlled vocabulary |
| Keyword search | Case-insensitive substring match | Full-text search; possibly semantic search (see implementation document) |
| Group and compare | Grouping and cross-tabulation (pandas) | Same |
| Data quality checks | Column, identifier, link and source checks | Same, plus curation review and sample verification against sources |

All of these are conventional data methods. No AI or machine learning is used in the prototype.

## 5. Expected outputs

- A filtered set of findings, each with project, evidence type, caveats and source reference.
- Counts of projects, findings and themes for the current selection, explicitly described as dataset counts.
- A comparison view of findings from different projects on the same theme.
- An exportable table to support the officer's own review and drafting.

The output is an **evidence overview**, not a conclusion or recommendation.

## 6. Human review points

1. **Curation:** a curator or subject-matter expert checks that each finding accurately reflects its source before publication in the dataset.
2. **Selection:** the policy officer decides which topic, themes and projects are relevant.
3. **Verification:** the officer opens the source documents for findings they intend to use.
4. **Interpretation:** the officer, with expert colleagues where necessary, interprets agreements, tensions and gaps.
5. **Use:** the officer decides what is included in the briefing and how it is worded.

## 7. Validation approach

Validation would proceed in stages, using the prototype to make requirements concrete:

1. **Concept validation** - present the workflow and prototype to a small group of policy officers and F2P coordinators; confirm whether the problem and concept reflect their reality.
2. **Requirements validation** - review each requirement in [requirements/requirements.csv](../requirements/requirements.csv) in a workshop; confirm, amend or reject; update priorities and validation status.
3. **Data feasibility check** - with data teams and data owners, test whether findings for one real topic can be curated from available sources with acceptable effort and quality.
4. **Task-based user testing** - users complete defined tasks (e.g. "find and verify findings on flood resilience from at least three projects") with a version using real data.

## 8. Pilot success indicators

Indicative only; targets would be agreed with stakeholders.

- Users can find and verify relevant findings for a defined task faster than with their current approach (measured in task-based sessions).
- A sample check confirms that curated findings accurately reflect their sources (e.g. agreed accuracy threshold on a random sample).
- 100% of displayed findings have a working source reference.
- Users report that limitations and source links are clear enough to rely on the overview as a starting point.
- Curation effort per finding is known and judged sustainable by the service owner.
- Stakeholders agree on whether and how to scale beyond the pilot topic.

## 9. Dependencies and constraints

- Availability of, and access rights to, project outputs (including non-public deliverables).
- Capacity of curators or subject-matter experts to extract and check findings.
- Agreement on a metadata schema and controlled vocabulary for topics, themes and evidence types.
- Alignment with existing Commission platforms, tools and data governance rules.
- Engagement of policy officers, whose time is limited.
- Any future AI component would depend on approved tools and infrastructure and on evaluation against expert-curated data.
