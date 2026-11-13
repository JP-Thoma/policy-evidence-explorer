# User needs and requirements elicitation

**Question this document answers:** how would the initial business request be turned into validated, prioritised requirements, and what is currently known, assumed or still open?

No interviews, workshops or user tests have taken place. Everything below is a proposed method and a set of working hypotheses.

## 1. Known, assumed and to be validated

| Status | Content |
|---|---|
| **Known from the role and assignment** | DG RTD's Common Knowledge and Data Management Service (RTD.H5) supports Feedback to Policy (F2P), which aims to make evidence from EU-funded research and other sources usable in policy development and research programming. Research results are spread across many projects, deliverables, publications and datasets, in different formats and levels of detail. |
| **Assumed for the illustrative case** | A policy officer preparing a briefing needs to compare findings across several projects. Being able to trace each finding to its source matters more to this user than an automated summary. A curated collection of findings for one topic could be assembled with reasonable effort. The officer remains responsible for interpretation and drafting. |
| **To be validated** | Actual user tasks and their frequency; current workflow, tools and hand-offs; pain points and where time is lost; user groups and decision rights; which sources are available and under what conditions; the level of detail users need; constraints (time, access, confidentiality, existing platforms); user preferences on format and AI support; and what success would look like for each stakeholder group. |

The assumptions are deliberately narrow. If elicitation shows that the main problem lies elsewhere (for example, in finding projects rather than comparing findings), the concept and requirements would change accordingly.

## 2. Stakeholders

The roles below are proposed. Actual roles, responsibilities and decision rights would need to be confirmed with RTD.H5 and the policy units involved.

| Stakeholder | Assumed interest | Proposed involvement | To confirm |
|---|---|---|---|
| **Policy officers** (primary users) | Finding relevant, reliable and traceable evidence within tight deadlines. | Interviews, task observation, prototype sessions, pilot use. | Which units and tasks; time available to take part. |
| **F2P representatives and coordinators** | Making project results visible and usable in policy; consistency across F2P services. | Interviews, requirements workshop, prioritisation. | Who can act as business-side product owner. |
| **Data and AI service teams** | Feasibility, reuse of existing platforms and data, maintainability. | Feasibility sessions, data assessment, pilot design. | Existing tools and data pipelines that could be reused. |
| **Data owners and governance stakeholders** (e.g. data stewards, information management, data protection, legal) | Lawful and appropriate use of data; access rights; confidentiality of non-public deliverables; data quality. | Early consultation on access, reuse conditions and metadata. | Access rules per source; approval steps. |
| **Subject-matter experts** (e.g. scientific or project officers) | Faithful representation of research results and their limitations. | Curation and review of findings during the pilot. | Capacity and willingness to curate. |

## 3. Elicitation plan: activities and their outputs

Each activity is chosen for the specific output it produces. Together they move from understanding the problem to agreeing testable requirements.

| Activity | Participants | Purpose | Output |
|---|---|---|---|
| **1. Stakeholder interviews** (semi-structured, 45-60 min) | 4-6 policy officers; F2P coordinators; one data/governance contact | Understand tasks, pain points, expectations and constraints. | Interview notes; list of user needs with source; first view of priorities and constraints. |
| **2. Current workflow walkthrough** | Policy officer and supporting colleagues | Map how evidence is currently found, checked and used for one or two recent outputs. | Process map ("as-is"), hand-offs, bottlenecks, tools and sources used. |
| **3. Representative task observation** | 2-3 policy officers | Observe (or reconstruct) preparation of a briefing on a defined topic. | Concrete evidence needs, usability requirements, and a **baseline** of time and effort for later comparison. |
| **4. Requirements workshop** | Policy officers, F2P coordinators, data teams, governance contacts | Review the draft catalogue; confirm, amend or reject each requirement; agree priorities and acceptance criteria. | Prioritised requirements with agreed acceptance criteria; decision records; open issues. |
| **5. Prototype-based feedback** | Policy officers (and later pilot users) | Test the concept on defined tasks, first with synthetic data, then with real data. | Usability observations; refined or new requirements; evidence for or against the concept. |

Activities 1-3 can run in parallel over a few weeks. The workshop (4) follows once needs have been consolidated. Prototype sessions (5) can start early, because a concrete demonstrator usually produces more specific feedback than abstract questions.

## 4. Core elicitation questions

A short guide; interviews would follow the conversation rather than a script.

| Area | Example questions |
|---|---|
| **Policy task and decision context** | Which outputs do you prepare that rely on research evidence? Who uses them, and for what decision? How much time do you usually have? |
| **Current workflow and pain points** | How do you find evidence from EU-funded projects today? Which step takes longest? Can you describe a time when relevant evidence was missed or found too late? |
| **Evidence and information needs** | What level of detail do you need: projects, individual findings, data or full reports? Which attributes of a finding matter most (method, location, scale, date, limitations)? |
| **Outputs and usability** | What would a useful evidence overview look like for you? How would you reuse it in your drafting? |
| **Data availability and constraints** | Which sources must be covered for the service to be useful? Are relevant documents restricted? Who could curate and check findings? |
| **Quality, trust and governance** | What would you need to see before relying on a finding? How should conflicting evidence be shown? What safeguards would you expect from any AI support? |
| **Success criteria** | What would convince you that the service saves time or improves quality? What would make you stop using it? |

## 5. From elicitation to agreed requirements

The Business Analyst would manage the catalogue in [requirements/requirements.csv](../requirements/requirements.csv) as follows.

- **Document findings.** Record each need with its source (activity, role, date) in interview notes and a needs log. Keep users' statements separate from the analyst's interpretation.
- **Trace.** Link every requirement to at least one recorded need, and later to the pilot feature and evaluation activity that tests it. Requirements without a traceable need are questioned or removed.
- **Resolve conflicts.** Where needs conflict (for example, broad coverage versus verified quality), make the trade-off explicit, set out options with their consequences, and ask the business-side product owner to decide. Record the decision and rationale.
- **Confirm priorities.** Use MoSCoW in the workshop. A requirement is a *Must* only if the pilot would fail its purpose without it, not because it is easy to build or already exists in the prototype.
- **Update validation status.** Change the status from *Provisional* to *Validated*, *Amended* or *Rejected* only with a recorded decision.
- **Manage change.** After the workshop, the catalogue is baselined. Later changes are proposed, assessed for impact on scope and evaluation, approved by the product owner and recorded in a change log.

### Proposed decision record format

The CSV catalogue intentionally stays simple. In a real project, each validation decision would be recorded separately in a format such as the one below. **This is a template, not a completed record**; no such decision has been taken.

| Field | Content |
|---|---|
| Requirement | FR-07 - export of selected evidence |
| Source of need | [interview / workshop reference and date] |
| Stakeholders consulted | [roles] |
| Date of decision | [date] |
| Decision | [Validated / Amended / Rejected] |
| Rationale | [summary of reasons] |
| Priority | [previous] -> [agreed] |
| Agreed acceptance criterion | [final wording] |
| Follow-up | [open issues, owner] |

## 6. Catalogue revision history

These changes were made by the author during desk review. They are **not** stakeholder decisions.

| Version | Change | Reason |
|---|---|---|
| 0.2 | BR-01 reframed as a business objective (a reviewable, multi-project evidence overview); topic selection moved to new **FR-08**. | Topic selection is functional behaviour, not a business outcome. |
| 0.2 | Former NFR-03 (AI-assisted extraction, classification or synthesis) reclassified as **FR-09**; NFR-03 retired and not reused. | It describes future functionality, not a quality attribute. |
| 0.2 | FR-02 (filters) priority changed from Must to Should. | Grouping by theme (FR-03) delivers the core value on a small pilot corpus; filters become more important as it grows. |
| 0.2 | FR-04, DR-01 and DR-03 reworded. | Separates metadata completeness, synthetic provenance and real-world source verification. |
