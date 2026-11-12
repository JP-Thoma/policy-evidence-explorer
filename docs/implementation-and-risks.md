# Implementation approach and risks

This document outlines a pragmatic path from the current concept and prototype to a pilot and, if justified, a production service. It is a proposal for discussion, not a plan agreed with stakeholders.

## 1. Progression overview

| Phase | Purpose | Main output |
|---|---|---|
| **Concept and prototype** (current) | Make the service idea and provisional requirements concrete enough to discuss with users. | This repository: synthetic data, prototype, provisional requirements. |
| **Discovery and validation** | Confirm the problem, users, requirements and data availability. | Validated requirements, workflow map, data feasibility assessment. |
| **Pilot** | Test the service with real data on one topic and a small user group. | Curated dataset for one topic, pilot application, evaluation report. |
| **Production (if justified)** | Run a maintained service integrated with existing systems and governance. | Operational service, documented processes, ownership and support. |

## 2. Key activities

### User engagement
Involve a small, committed group of policy officers and F2P coordinators from the start. Use short, task-focused sessions to respect their time. Report back what was changed as a result of their input.

### Requirements validation
Review the provisional catalogue in a workshop; record decisions and update `validation_status`. Keep acceptance criteria testable and link each to a pilot evaluation activity.

### Data availability and quality assessment
For the pilot topic, identify candidate sources, check access conditions and assess metadata quality. Curate a sample of findings and measure effort and consistency between curators before committing to a full topic.

### Pilot scope
One policy topic, a limited number of projects (for example 20-40) and a small user group. Read-only access to curated findings. No automated extraction in the first iteration, so that a reliable expert-curated baseline exists.

### Roles and expertise
| Role | Contribution |
|---|---|
| Business Analyst | Elicitation, requirements, process mapping, evaluation design, stakeholder communication. |
| Product owner (business side) | Prioritisation and acceptance decisions. |
| Subject-matter experts / curators | Extraction and verification of findings, theme definitions. |
| Data engineer / developer | Data model, pipeline, application. |
| Data governance and legal contacts | Access, confidentiality, data protection, retention. |
| AI specialist (later phase) | Evaluation of AI-assisted methods against the curated baseline. |

### Evaluation
Task-based user sessions, a sample accuracy check of findings against sources, measurement of curation effort, and a short user questionnaire. Compare results against success indicators agreed at the start of the pilot.

### Documentation and governance
Document the data model, controlled vocabulary, curation guidelines, provenance of each record, access rules and change history. Define ownership of the dataset and the process for corrections.

### Adoption
Integrate into existing ways of working rather than adding another standalone tool where possible. Provide short guidance, identify early adopters and collect feedback continuously.

### Production considerations
Hosting on approved infrastructure, authentication and access control, integration with existing research and document repositories, accessibility, maintenance and support model, monitoring of usage and data freshness, and a sustainable curation process.

## 3. Risks and mitigations

| Risk | Possible impact | Mitigation |
|---|---|---|
| **Incomplete source coverage** | Users assume the overview is complete and miss relevant evidence. | Publish coverage criteria and date of last update with the dataset; show counts as dataset counts; state clearly what is not covered. |
| **Poor or inconsistent metadata** | Filters and comparisons give misleading results. | Agree a metadata schema and controlled vocabulary; run automated quality checks; double-curate a sample to measure consistency. |
| **Misinterpretation of research findings** | Findings are used out of context or overstated in policy documents. | Display evidence type and caveats with every finding; use cautious wording; involve subject-matter experts in curation; keep the human review step explicit. |
| **Weak source traceability** | Findings cannot be verified, undermining trust. | Make a document-level reference mandatory; exclude records without one (as in the prototype); test link validity regularly. |
| **Biased selection of evidence** | Overview favours certain projects, methods or viewpoints. | Document selection criteria; show where themes have little or no coverage; review dataset composition with experts; allow users to see all findings, not only a summary. |
| **Confidentiality or access issues** | Non-public material is exposed or cannot be used. | Consult data owners early; record access conditions per source; apply access control in pilot and production; start the pilot with public material if needed. |
| **Automation bias** | Users rely on the tool's presentation instead of checking sources. | Present the overview as a starting point; require source verification in guidance; avoid scores or rankings that imply quality judgements. |
| **AI-generated inaccuracies (future version)** | Extracted or summarised content misstates or invents findings. | Ground any output in cited source passages; label AI-generated content clearly; evaluate against the curated baseline before use; keep human review of all AI-extracted findings. |

## 4. AI as a possible future enhancement

The current prototype does **not** use AI. All functions use conventional data handling: structured fields, filtering, grouping and keyword search.

AI methods could be considered later, once a validated, expert-curated dataset exists against which they can be evaluated:

| Possible AI use | Potential benefit | Main caution |
|---|---|---|
| **Semantic retrieval** | Find relevant findings even when different terms are used. | Results must still be traceable and explainable; relevance should be checked by users. |
| **Thematic classification** | Suggest themes for new findings to reduce curation effort. | Suggestions should be reviewed by curators; classification errors propagate into comparisons. |
| **Extraction of candidate findings** | Propose findings from long project reports. | High risk of omission or misstatement; human verification is essential. |
| **Source-grounded synthesis** | Draft short summaries of what several findings say, with citations. | Risk of overgeneralisation and of blurring findings and interpretation; must cite sources and be labelled as generated. |

**Where conventional methods remain sufficient:** filtering by agreed metadata, counting and cross-tabulation, keyword search over a modest dataset, data quality checks and export. For a pilot with one topic and a curated dataset, these methods are likely to meet the core needs. AI is most likely to add value in scaling the curation process, which is also where its risks are highest.

Any AI component would need to use approved tools and infrastructure, comply with applicable Commission rules and EU legislation on data protection and AI, and be evaluated with measurable acceptance criteria before use.
