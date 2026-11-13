# Implementation, data readiness and risks

**Question this document answers:** how would the concept move from a prototype to a bounded real-data pilot and, if justified, wider use; what must the data look like; where might AI add value; and what could go wrong?

## 1. Implementation sequence

Each phase ends with a decision, so that effort is only committed once the previous step has produced evidence.

| Phase | Purpose | Main output | Decision at the end |
|---|---|---|---|
| **1. Concept and provisional requirements** (current) | Make the idea concrete enough to discuss with users. | This repository: concept, provisional catalogue, synthetic prototype. | Is the problem worth investigating with stakeholders? |
| **2. Stakeholder discovery and requirements validation** | Confirm users, tasks, pain points and priorities. | Validated requirements, as-is process map, task baseline, decision records. | Is the assumed need real, and for whom? |
| **3. Data feasibility and source assessment** | Check whether sources for one topic are available, accessible and reusable. | Source inventory, access conditions, data-readiness assessment (section 4), curation effort estimate from a small sample. | Can a reliable evidence base be built within constraints? |
| **4. Bounded real-data pilot** | Test the service with real data and real users. | Curated dataset for one topic, pilot application, user guidance. | - |
| **5. Evaluation and decision** | Assess relevance, fidelity, efficiency, usability, feasibility and adoption. | Evaluation report against agreed thresholds ([concept-and-validation.md, section 7](concept-and-validation.md#7-pilot-evaluation-framework)). | GO / REVISE / STOP |
| **6. Wider implementation, if justified** | Extend to further topics and integrate with existing systems. | Operational service with owner, processes and support. | Ongoing review |

## 2. Proposed pilot scope

**One policy topic with several relevant themes.** The prototype contains two synthetic topics to show that the design is not tied to a single subject; the first real-data pilot would deliberately narrow the scope to one.

The pilot would include:

- a limited corpus of real project outputs, selected against documented criteria;
- findings curated by subject-matter experts against an agreed schema;
- working, document-level source references;
- a small group of representative policy users and a defined briefing task;
- agreed review responsibilities (see [concept-and-validation.md, section 6](concept-and-validation.md#6-human-review-points));
- a manageable evaluation plan with thresholds agreed in advance.

Advanced AI is **not** a prerequisite. The pilot tests whether a reliable evidence base is useful and feasible; that question has to be answered first.

## 3. Roles

| Role | Contribution |
|---|---|
| **Business Analyst** | Elicitation, process mapping, requirements and traceability, evaluation design, stakeholder communication. |
| **Business-side product owner** | Prioritisation, acceptance decisions and the GO / REVISE / STOP decision. |
| **Policy officers** | Define the pilot task, use the service, provide feedback. |
| **F2P representatives** | Link to F2P processes, help select the topic and engage users. |
| **Evidence curators / subject-matter experts** | Select sources, extract and check findings, define themes. |
| **Data engineer / developer** | Data model, quality checks, application and integration. |
| **Data governance and legal stakeholders** | Access, confidentiality, reuse conditions, data protection. |
| **AI specialist** (only if later justified) | Evaluate AI options against the curated reference data. |

How these roles map onto actual Commission staff and teams would need to be agreed.

## 4. Data readiness for a real-data pilot (FAIR-oriented)

The synthetic prototype is **not** FAIR-compliant and does not claim to be. The assessment below sets out what a credible real-data pilot would need, using the FAIR principles (Findable, Accessible, Interoperable, Reusable) as a practical checklist.

| Principle | What the pilot would need | Prototype today | Gap to close |
|---|---|---|---|
| **Findable** | Persistent project and document identifiers; descriptive metadata; consistent references down to section or page. | Stable synthetic IDs (`SYN-P..`, `SYN-F..`, `SYN-SRC-..`); document titles. | Real identifiers; section-level references. |
| **Accessible** | Working links; clear distinction between public and restricted material; recorded access conditions and permissions. | No links; all data synthetic and public. | Links; access conditions per source; access control (NFR-01). |
| **Interoperable** | Common metadata fields; controlled vocabularies for topics, themes and evidence types; standard formats; alignment with existing classifications where available. | Consistent fields in CSV; theme and evidence-type values not governed by a vocabulary. | Agreed vocabularies and schema (DR-02). |
| **Reusable** | Provenance; methodological context; known limitations; licence and reuse conditions; curation and review history. | Evidence type and caveat per finding; "synthetic" status label. | Licence, curator, review date, verification status, methodological context. |

**Metadata in the prototype:** project ID, title, topic, description, research area; finding ID, project link, title, description, topic, theme, evidence type, limitation, source document, source reference, data status.

**Additional metadata a pilot would need:** research setting; geographic context; study period; methodology; precise document and section reference; document access conditions; licence or reuse conditions; curator; review date; verification status. These fields are deliberately **not** added to the synthetic dataset; they are pilot design requirements (DR-02, DR-03).

## 5. Data and AI approach

### Where conventional methods are sufficient

The prototype uses structured fields, exact-match filtering, keyword search, grouping, cross-tabulation, data quality checks and CSV export. For a pilot on one topic with a curated corpus of modest size, these methods are likely to meet the core needs: users choose from known themes, the corpus can be browsed, and the main risk lies in data quality, not retrieval.

### Where AI might add value later (FR-09)

| Capability | Problem it might address | Potential benefit | Data prerequisites | Main risks | Human review and evaluation |
|---|---|---|---|---|---|
| **Semantic retrieval** | Relevant findings are missed because projects use different terms. | Better recall as the corpus grows. | Curated findings with consistent metadata. | Opaque relevance; false confidence in completeness. | Users judge relevance; compare recall against curated test queries. |
| **Thematic classification** | Assigning themes to many new findings is slow and inconsistent. | Faster, more consistent curation. | Agreed vocabulary; labelled examples. | Misclassification distorts comparisons. | Curators confirm every suggestion; measure agreement with expert labels. |
| **Candidate finding extraction** | Long reports make manual extraction costly. | Reduced curation effort. | Machine-readable documents; access rights; expert-curated reference sample. | Omissions; misstatements; findings taken out of context. | Curators verify each candidate; compare with expert extraction for omissions and errors. |
| **Source-grounded synthesis** | Users want a quick view of how findings compare. | Faster orientation across many projects. | Verified findings with section-level references. | Overgeneralisation; blurring of finding and interpretation; inaccurate citations. | Clearly labelled as generated; every statement cites sources; checked for citation accuracy. |

The order of these capabilities reflects increasing risk. A reliable data foundation and a verified user need are prerequisites for deciding where AI adds value; AI should not be introduced simply because it is technically possible. Any AI component would also need approved tools and infrastructure and compliance with applicable Commission rules and EU legislation on data protection and AI.

## 6. Governance and documentation

- Publish the data model, controlled vocabularies, curation guidelines and coverage criteria with the dataset.
- Record provenance and review history for each finding.
- Agree ownership of the evidence base and a process for reporting and correcting errors.
- Keep the requirements catalogue, decision records and change log up to date (see [user-needs.md](user-needs.md)).

## 7. Adoption

- **Fit with existing work:** design around a real briefing task identified in discovery, and link to existing tools rather than adding a separate destination where possible.
- **Early involvement:** involve the same small group of policy officers from discovery to pilot, so that they recognise their input.
- **Guidance:** short user guidance explaining what the overview is (a starting point) and what it is not (a verified conclusion).
- **Feedback:** a simple channel for reporting errors and requesting sources, reviewed regularly.
- **Ownership and maintenance:** a named service owner, and an agreed process and resourcing for adding and updating findings.

## 8. Considerations for wider implementation

Hosting on approved infrastructure; authentication and access control; integration with existing research and document repositories; accessibility; support model; monitoring of usage and data currency; and sustainable curation capacity. These would be scoped only after a GO decision.

## 9. Risks and mitigations

| Risk | Possible impact | Mitigation |
|---|---|---|
| **Incomplete source coverage** | Users assume the overview is complete and miss evidence. | Publish coverage criteria and last update date; label counts as dataset coverage (as the prototype does); show themes with little coverage. |
| **Poor or inconsistent metadata** | Filters and comparisons mislead. | Agreed schema and vocabularies; automated checks; double-curate a sample to measure consistency. |
| **Misinterpretation of findings** | Findings are used out of context or overstated. | Show evidence type and caveats with every finding; involve experts in curation; keep the officer's review step explicit in guidance. |
| **Weak source traceability** | Findings cannot be verified, undermining trust. | Make section-level references mandatory; exclude records without them (as the prototype does); test links regularly. |
| **Biased selection of evidence** | The overview favours certain projects, methods or viewpoints. | Documented selection criteria; expert review of dataset composition; show all findings, not only a summary. |
| **Confidentiality or access issues** | Restricted material is exposed, or cannot be used. | Consult data owners early; record access conditions per source; start with public material if needed. |
| **Automation bias** | Users rely on the presentation instead of checking sources. | Present the overview as a starting point; require source checks in guidance; avoid scores or rankings that imply quality judgements. |
| **AI-generated inaccuracies (future)** | Extracted or synthesised content misstates or invents findings. | Ground outputs in cited passages; label generated content; evaluate against curated reference data before use; human review of all AI output. |
| **Insufficient user or curator time** | Pilot cannot be run or evaluated properly. | Agree time commitments with management before the pilot; keep sessions short and task-based. |
