# User needs and requirements elicitation approach

This document describes how user needs for the Policy Evidence Explorer **would be** gathered and validated. No interviews, workshops or user tests have been carried out. All needs and requirements in this repository are provisional working hypotheses.

## 1. Starting point: what is known, assumed and open

| Type | Content |
|---|---|
| **Known from the role context** | DG RTD's Common Knowledge and Data Management Service supports Feedback to Policy (F2P) activities that channel evidence from EU-funded research into policy development and research programming. Research results are spread across many projects, deliverables, publications and datasets in different formats. |
| **Working assumptions** | Policy officers preparing briefings need to identify, compare and verify findings from several projects within limited time. They value traceability to sources more than automated summaries. A structured, curated dataset of findings could be produced for at least one pilot topic. Policy officers remain responsible for interpretation and drafting. |
| **Questions requiring user validation** | Which policy tasks are most frequent and time-critical? How is evidence currently gathered and by whom? What level of granularity (project, deliverable, individual finding) is useful? Which sources are accessible and under what conditions? What would make users trust, or distrust, such a service? What does success look like for each stakeholder group? |

The illustrative use case (a policy officer preparing a briefing on urban climate adaptation) is an assumption chosen to make the concept concrete. It is not a confirmed requirement.

## 2. Stakeholders

The roles below are proposed. Actual roles, responsibilities and decision rights would need to be confirmed with DG RTD.

| Stakeholder | Assumed interest | Proposed involvement |
|---|---|---|
| **Policy officers** (primary users) | Finding relevant, reliable and traceable evidence quickly for briefings and policy input. | Interviews, task walkthroughs, prototype feedback, usability testing. |
| **F2P representatives and coordinators** | Making project results more visible and usable in policy; consistency of F2P services. | Interviews, validation workshop, prioritisation of requirements. |
| **Data and AI service teams** | Feasibility, data pipelines, reuse of existing platforms and tools, maintainability. | Technical feasibility sessions, data availability assessment, pilot design. |
| **Data owners and governance stakeholders** (e.g. data stewards, information management, data protection, legal) | Lawful and appropriate use of data; access rights; confidentiality of non-public deliverables; data quality. | Early consultation on access and confidentiality; review of governance requirements. |
| **Subject-matter experts** (possible secondary stakeholders, e.g. scientific officers) | Correct representation of research results and their limitations. | Review of curated findings and comparison views during the pilot. |

## 3. Proposed engagement methods

1. **Initial stakeholder interviews** (semi-structured, 45-60 minutes) with a small number of policy officers and F2P coordinators, to understand tasks, pain points and expectations.
2. **Review of the current evidence workflow**: map how evidence is currently found, assessed and used for one or two recent policy outputs, including tools, sources, hand-offs and time spent.
3. **Walkthrough of a representative policy task**: observe or reconstruct how a policy officer would prepare a briefing on a defined topic, noting where evidence is hard to find, compare or verify.
4. **Requirements validation workshop**: present the provisional requirements catalogue ([requirements/requirements.csv](../requirements/requirements.csv)), confirm or reject each requirement, agree priorities (MoSCoW) and acceptance criteria.
5. **Prototype-based user feedback**: use this prototype (and later a version with real data) in short sessions where users complete defined tasks and comment on usefulness, clarity and trust.

Findings from each step would be recorded, and the requirements catalogue updated with a changed `validation_status` and a note of the source of validation.

## 4. Elicitation questions

### 4.1 Policy task and decision context
- Which policy outputs do you prepare that rely on research evidence (briefings, impact assessments, programme design, speeches)?
- How often do you prepare them, and how much time do you typically have?
- Who uses your output, and what decisions does it inform?
- Can you describe a recent task where research evidence was important?

### 4.2 Current workflow and pain points
- How do you currently find evidence from EU-funded projects? Which tools, databases or colleagues do you rely on?
- Which steps take the most time?
- Have you ever missed relevant evidence or found it too late? What happened?
- How do you compare results from different projects today?

### 4.3 Evidence and information needs
- What level of detail is useful to you: project summaries, individual findings, data, or full reports?
- Which attributes of a finding matter most (method, location, scale, date, evidence type, limitations)?
- How important is it to see agreements and disagreements between projects?
- Do you also need evidence from non-EU-funded or external sources?

### 4.4 Expected outputs and usability
- What would an ideal evidence overview look like for you? Could you sketch or describe one?
- In which format would you reuse the results (table, short text, export to a document)?
- What would make a tool too complicated to use in your daily work?
- Would you use such a service on your own, or with support from F2P or data teams?

### 4.5 Data availability and constraints
- Which sources would need to be covered for the service to be useful?
- Are some relevant documents non-public or restricted? Who decides on access?
- Who could curate or check findings, and with what effort?
- Are existing classifications or taxonomies available for topics and themes?

### 4.6 Quality, trust and governance
- What would you need to see before relying on a finding in your work?
- How should limitations or conflicting evidence be presented?
- How would you feel about AI-generated summaries or classifications? What safeguards would you expect?
- Who should be accountable for the content of the evidence base?

### 4.7 Success criteria
- What would convince you that the service saves time or improves quality?
- How could we measure whether a pilot has succeeded?
- What would make you stop using the service?

## 5. From needs to requirements

Each user need captured during elicitation is translated into one or more requirements with:

- a unique identifier and category (Business, Functional, Data, Non-functional);
- a MoSCoW priority agreed with stakeholders;
- an observable, testable acceptance criterion;
- a validation status (initially *Provisional - requires user confirmation*);
- a note of whether and how the prototype covers it.

The current catalogue in [requirements/requirements.csv](../requirements/requirements.csv) is a first draft based on the working assumptions above. The prototype is intended as a tool to test these assumptions with users, not as evidence that the requirements are correct.
