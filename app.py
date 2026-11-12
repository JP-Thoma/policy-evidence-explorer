"""Policy Evidence Explorer - illustrative Streamlit proof of concept.

Requirement IDs in comments refer to requirements/requirements.csv.
Run with:  streamlit run app.py
"""

from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st

import data_utils as du

st.set_page_config(
    page_title="Policy Evidence Explorer",
    page_icon=":material/library_books:",
    layout="wide",
    initial_sidebar_state="expanded",
)

SYNTHETIC_NOTICE = (
    "Illustrative proof of concept using synthetic research data. "
    "Not an official European Commission service."
)

FILTER_DEFAULTS: dict[str, list[str] | str] = {
    "themes": [],
    "projects": [],
    "evidence_types": [],
    "keyword": "",
}

# Public-sector look (blue/yellow accents, Arial, flat panels) without official logos or emblems.
PAGE_CSS = """
<style>
[data-testid="stMainBlockContainer"] { max-width: 1240px; padding-top: 4rem; }

.pee-masthead { background: #004494; color: #ffffff; padding: 1.5rem 1.75rem 1.35rem;
  border-bottom: 5px solid #ffd617; border-radius: 4px 4px 0 0; }
.pee-masthead__eyebrow { font-size: .78rem; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; color: #c9d7f0; margin: 0 0 .4rem; }
.pee-masthead h1.pee-masthead__title { font-size: 2.1rem; font-weight: 700; line-height: 1.2;
  margin: 0; padding: 0; color: #ffffff; }
.pee-masthead__subtitle { font-size: 1.05rem; margin: .45rem 0 0; color: #e6ecf7; }

.pee-notice { display: flex; gap: .75rem; align-items: baseline; background: #fff8d6;
  border-left: 5px solid #ffd617; padding: .7rem 1rem; color: #262b38; font-size: .95rem; }
.pee-notice__label { font-weight: 700; white-space: nowrap; }

.pee-section { margin: 1.6rem 0 .4rem; }
.pee-section__title { font-size: 1.4rem; font-weight: 700; color: #262b38; padding-bottom: .45rem;
  border-bottom: 1px solid #d9e1f2; position: relative; }
.pee-section__title::after { content: ""; position: absolute; left: 0; bottom: -1px; width: 3rem;
  height: 3px; background: #ffd617; }
.pee-section__lead { color: #4a5568; margin: .55rem 0 0; font-size: .95rem; }

.pee-scope { margin: 0 0 .55rem; color: #4a5568; font-size: .95rem; }
.pee-filters { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; font-size: .85rem;
  color: #4a5568; margin: .25rem 0; }

.pee-tag { display: inline-block; font-size: .75rem; font-weight: 700; padding: .15rem .55rem;
  border-radius: 2px; background: #e6ecf7; color: #004494; }
.pee-tag--neutral { background: #eef0f3; color: #404b5a; }
.pee-tag--synthetic { background: #fff3b0; color: #5c4a00; }
.pee-muted { color: #6b7280; font-size: .85rem; }
.pee-ref { font-family: Consolas, "Courier New", monospace; font-size: .82rem; background: #f3f6fc;
  border: 1px solid #d9e1f2; padding: 0 .3rem; border-radius: 2px; color: #262b38; }

.pee-theme-heading { display: flex; justify-content: space-between; align-items: baseline;
  margin: 1.1rem 0 .6rem; padding-bottom: .3rem; border-bottom: 2px solid #004494; }
.pee-theme-heading__title { font-size: 1.1rem; font-weight: 700; color: #004494; }

.pee-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: .9rem; }

.pee-card { background: #ffffff; border: 1px solid #d9e1f2; border-left: 4px solid #004494;
  border-radius: 4px; padding: 1rem 1.2rem; color: #262b38; }
.pee-tags { display: flex; flex-wrap: wrap; gap: .35rem; margin-bottom: .6rem; }
.pee-card__title { font-size: 1.05rem; font-weight: 700; line-height: 1.35; margin: 0 0 .5rem; }
.pee-card__label { font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em;
  color: #6b7280; margin: 0 0 .2rem; }
.pee-card__text { margin: 0 0 .75rem; line-height: 1.5; font-size: .93rem; }
.pee-caveat { background: #fdf3e7; border-left: 3px solid #e57200; padding: .5rem .75rem;
  font-size: .88rem; line-height: 1.45; }
.pee-caveat__label { display: block; font-weight: 700; font-size: .72rem; text-transform: uppercase;
  letter-spacing: .06em; color: #8a4500; margin-bottom: .15rem; }
.pee-source { display: grid; grid-template-columns: max-content 1fr; gap: .25rem 1rem;
  font-size: .84rem; margin: .8rem 0 0; padding: .65rem 0 0 !important; border-top: 1px solid #e6ecf7; }
.pee-source dt { color: #6b7280; margin: 0; padding: 0; font-weight: 400; }
.pee-source dd { margin: 0; padding: 0; color: #262b38; }

.pee-panel { background: #f8f9fc; border: 1px solid #d9e1f2; border-top: 4px solid #004494;
  border-radius: 4px; padding: .9rem 1.1rem; color: #262b38; }
.pee-panel__project { font-weight: 700; font-size: 1rem; line-height: 1.35; }
.pee-panel__item { padding: .7rem 0 .2rem; margin-top: .6rem; border-top: 1px solid #d9e1f2; }
.pee-panel__finding { font-weight: 700; font-size: .93rem; margin-bottom: .25rem; }
.pee-panel__desc { font-size: .88rem; line-height: 1.45; margin-bottom: .4rem; }
.pee-panel__meta { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; margin-bottom: .35rem; }
.pee-panel__caveat { font-size: .84rem; color: #8a4500; line-height: 1.4; }

.pee-dist { border: 1px solid #d9e1f2; border-radius: 4px; padding: .9rem 1.1rem; background: #ffffff; }
.pee-dist__title { font-weight: 700; font-size: .92rem; margin-bottom: .6rem; color: #262b38; }
.pee-bar { display: grid; grid-template-columns: minmax(150px, 40%) 1fr 2rem; gap: .6rem;
  align-items: center; font-size: .86rem; margin: .3rem 0; color: #262b38; }
.pee-bar__track { background: #eef2f9; height: .7rem; border-radius: 2px; }
.pee-bar__fill { background: #004494; height: 100%; border-radius: 2px; }
.pee-bar__value { text-align: right; font-weight: 700; }

.pee-matrix { border-collapse: collapse; width: 100%; font-size: .86rem; color: #262b38; }
.pee-matrix th, .pee-matrix td { border: 1px solid #d9e1f2; padding: .4rem .55rem; text-align: center; }
.pee-matrix thead th { background: #e6ecf7; font-weight: 700; }
.pee-matrix tbody th { text-align: left; font-weight: 700; background: #f8f9fc; }
.pee-matrix td.pee-matrix__empty { color: #9aa3b2; }

.pee-two-col { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem; }
.pee-box { border: 1px solid #d9e1f2; border-radius: 4px; padding: 1rem 1.2rem;
  background: #ffffff; color: #262b38; font-size: .93rem; line-height: 1.5; }
.pee-box--blue { background: #f3f6fc; border-left: 4px solid #004494; }
.pee-box__title { font-weight: 700; font-size: 1rem; margin-bottom: .5rem; }
.pee-box ul, .pee-box ol { margin: 0; padding-left: 1.2rem; }
.pee-box li { margin-bottom: .4rem; }

.pee-footer { margin-top: 2.5rem; background: #004494; color: #e6ecf7; padding: 1.1rem 1.5rem;
  border-top: 5px solid #ffd617; font-size: .85rem; line-height: 1.5; }
.pee-footer strong { color: #ffffff; }
</style>
"""


@st.cache_data
def load_evidence() -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    projects = du.load_projects()
    findings = du.load_findings()
    issues = du.validate_data(projects, findings)
    evidence = du.prepare_evidence(findings, projects)
    return projects, evidence, issues


def esc(value: object) -> str:
    """HTML-escape data values before inserting them into markup."""
    return escape(str(value))


def reset_filters() -> None:
    for key, value in FILTER_DEFAULTS.items():
        st.session_state[key] = list(value) if isinstance(value, list) else value


def keep_valid_selection(key: str, options: list[str]) -> None:
    """Drop previously selected values that are no longer available (e.g. after a topic change)."""
    if key in st.session_state:
        st.session_state[key] = [v for v in st.session_state[key] if v in options]


def section_heading(title: str, lead: str = "") -> None:
    lead_html = f'<p class="pee-section__lead">{esc(lead)}</p>' if lead else ""
    st.html(
        f'<div class="pee-section"><div class="pee-section__title" role="heading" aria-level="2">'
        f"{esc(title)}</div>{lead_html}</div>"
    )


def finding_card_html(row: pd.Series) -> str:
    """Finding card with context, caveat and source (FR-04, FR-05, FR-06)."""
    return (
        '<article class="pee-card">'
        '<div class="pee-tags">'
        f'<span class="pee-tag">{esc(row["thematic_category"])}</span>'
        f'<span class="pee-tag pee-tag--neutral">{esc(row["evidence_type"])}</span>'
        '<span class="pee-tag pee-tag--synthetic">Synthetic</span>'
        "</div>"
        f'<div class="pee-card__title" role="heading" aria-level="3">{esc(row["finding_title"])}</div>'
        '<div class="pee-card__label">Reported finding</div>'
        f'<p class="pee-card__text">{esc(row["finding_description"])}</p>'
        '<div class="pee-caveat"><span class="pee-caveat__label">Limitations and caveats</span>'
        f'{esc(row["evidence_limitation"])}</div>'
        '<dl class="pee-source">'
        f'<dt>Project</dt><dd>{esc(row["project_title"])} '
        f'<span class="pee-muted">({esc(row["project_id"])})</span></dd>'
        f'<dt>Policy topic</dt><dd>{esc(row["policy_topic"])}</dd>'
        f'<dt>Source document</dt><dd>{esc(row["source_document"])}</dd>'
        f'<dt>Source reference</dt><dd><span class="pee-ref">{esc(row["source_reference"])}</span> '
        f'<span class="pee-muted">Finding {esc(row["finding_id"])}</span></dd>'
        "</dl></article>"
    )


def comparison_panel_html(group: pd.DataFrame) -> str:
    first = group.iloc[0]
    items = "".join(
        '<div class="pee-panel__item">'
        f'<div class="pee-panel__finding">{esc(r.finding_title)}</div>'
        f'<div class="pee-panel__desc">{esc(r.finding_description)}</div>'
        '<div class="pee-panel__meta">'
        f'<span class="pee-tag pee-tag--neutral">{esc(r.evidence_type)}</span>'
        f'<span class="pee-ref">{esc(r.source_reference)}</span></div>'
        f'<div class="pee-panel__caveat"><strong>Caveat:</strong> {esc(r.evidence_limitation)}</div>'
        "</div>"
        for r in group.itertuples()
    )
    count = len(group)
    return (
        '<section class="pee-panel">'
        f'<div class="pee-panel__project" role="heading" aria-level="3">{esc(first["project_title"])}</div>'
        f'<div class="pee-muted">{esc(first["project_id"])} &middot; {count} '
        f'finding{"s" if count != 1 else ""} on this theme</div>'
        f"{items}</section>"
    )


def distribution_html(title: str, counts: pd.Series) -> str:
    """Simple horizontal bar list; avoids chart axes with fractional ticks for small counts."""
    peak = max(int(counts.max()), 1)
    rows = "".join(
        '<div class="pee-bar">'
        f"<div>{esc(label)}</div>"
        f'<div class="pee-bar__track"><div class="pee-bar__fill" style="width:{int(value) / peak * 100:.0f}%">'
        "</div></div>"
        f'<div class="pee-bar__value">{int(value)}</div></div>'
        for label, value in counts.items()
    )
    return f'<div class="pee-dist"><div class="pee-dist__title">{esc(title)}</div>{rows}</div>'


def coverage_matrix_html(matrix: pd.DataFrame, titles: dict[str, str]) -> str:
    header = "".join(
        f'<th scope="col" title="{esc(titles.get(pid, pid))}">{esc(pid)}</th>' for pid in matrix.columns
    )
    body = ""
    for theme, row in matrix.iterrows():
        cells = "".join(
            f"<td>{int(v)}</td>" if v else '<td class="pee-matrix__empty">&ndash;</td>' for v in row
        )
        body += f'<tr><th scope="row">{esc(theme)}</th>{cells}</tr>'
    return (
        '<table class="pee-matrix"><thead><tr><th scope="col">Theme</th>'
        f"{header}</tr></thead><tbody>{body}</tbody></table>"
    )


def project_card_html(project: pd.Series) -> str:
    return (
        '<article class="pee-card">'
        f'<div class="pee-tags"><span class="pee-tag pee-tag--neutral">{esc(project["research_area"])}</span>'
        '<span class="pee-tag pee-tag--synthetic">Synthetic</span></div>'
        f'<div class="pee-card__title" role="heading" aria-level="3">{esc(project["project_title"])}</div>'
        f'<p class="pee-card__text">{esc(project["short_description"])}</p>'
        '<dl class="pee-source">'
        f'<dt>Project ID</dt><dd><span class="pee-ref">{esc(project["project_id"])}</span></dd>'
        f'<dt>Findings in view</dt><dd>{int(project["findings_in_view"])}</dd>'
        "</dl></article>"
    )


# --- Data loading -------------------------------------------------------------

try:
    projects, evidence, data_issues = load_evidence()
except (FileNotFoundError, ValueError) as exc:
    st.error(f"The data could not be loaded: {exc}")
    st.stop()

# --- Header -------------------------------------------------------------------

st.html(PAGE_CSS)
st.html(
    '<header class="pee-masthead">'
    '<div class="pee-masthead__eyebrow">Research and innovation evidence &middot; Proof of concept</div>'
    '<h1 class="pee-masthead__title">Policy Evidence Explorer</h1>'
    '<p class="pee-masthead__subtitle">Exploring research findings across projects to support '
    "evidence-informed policy work.</p></header>"
    f'<div class="pee-notice" role="note"><span class="pee-notice__label">Notice</span>'
    f"<span>{esc(SYNTHETIC_NOTICE)}</span></div>"
)

if data_issues:
    with st.expander("Data quality notice: some records were excluded", icon=":material/warning:"):
        st.write(
            "The following issues were detected. Findings without a valid project link "
            "or source reference are not displayed."
        )
        for issue in data_issues:
            st.write(f"- {issue}")

if evidence.empty:
    st.warning("No traceable findings are available in the dataset.")
    st.stop()

for key, value in FILTER_DEFAULTS.items():
    st.session_state.setdefault(key, list(value) if isinstance(value, list) else value)

# --- A. Policy topic selection (BR-01, FR-01, FR-02) --------------------------

section_heading(
    "1. Policy topic",
    "Choose the policy topic of your briefing, then refine the selection with the filters in the sidebar.",
)

# Topic order follows the projects file; options come from the data, not the code.
available_topics = set(evidence["policy_topic"])
topics = [t for t in projects["policy_topic"].drop_duplicates() if t in available_topics]

col_topic, col_scope = st.columns([2, 3], vertical_alignment="bottom")
with col_topic:
    topic = st.selectbox("Policy topic", topics, key="topic")
topic_evidence = du.filter_findings(evidence, topic=topic)
topic_counts = du.summarise(topic_evidence)
with col_scope:
    st.html(
        f'<p class="pee-scope">The synthetic dataset for this topic contains '
        f'<strong>{topic_counts["projects"]}</strong> projects and '
        f'<strong>{topic_counts["findings"]}</strong> findings across '
        f'<strong>{topic_counts["themes"]}</strong> thematic categories.</p>'
    )

project_titles = (
    topic_evidence.drop_duplicates("project_id").set_index("project_id")["project_title"].to_dict()
)

with st.sidebar:
    st.markdown("### Refine the selection")
    st.caption(f"Filters apply within the selected topic: **{topic}**. Leave a filter empty to include all.")

    # Options are derived from the data, so new themes or projects need no code changes.
    theme_options = sorted(topic_evidence["thematic_category"].unique())
    keep_valid_selection("themes", theme_options)
    selected_themes = st.multiselect(
        "Thematic category", theme_options, key="themes", placeholder="All themes"
    )

    project_options = sorted(project_titles)
    keep_valid_selection("projects", project_options)
    selected_projects = st.multiselect(
        "Project",
        project_options,
        format_func=lambda pid: project_titles.get(pid, pid),
        key="projects",
        placeholder="All projects",
    )

    type_options = sorted(topic_evidence["evidence_type"].unique())
    keep_valid_selection("evidence_types", type_options)
    selected_types = st.multiselect(
        "Evidence type", type_options, key="evidence_types", placeholder="All evidence types"
    )

    keyword = st.text_input(
        "Keyword", key="keyword", placeholder="Search titles, descriptions, caveats"
    )

    st.button(
        "Reset filters",
        key="reset_filters",
        on_click=reset_filters,
        icon=":material/restart_alt:",
        width="stretch",
    )
    st.divider()
    st.caption(SYNTHETIC_NOTICE)

filtered = du.filter_findings(
    evidence,
    topic=topic,
    themes=selected_themes,
    project_ids=selected_projects,
    evidence_types=selected_types,
    keyword=keyword,
)

active = (
    [f"Theme: {t}" for t in selected_themes]
    + [f"Project: {pid}" for pid in selected_projects]
    + [f"Evidence type: {t}" for t in selected_types]
    + ([f"Keyword: {keyword.strip()}"] if keyword.strip() else [])
)
if active:
    chips = "".join(f'<span class="pee-tag">{esc(a)}</span>' for a in active)
    st.html(f'<div class="pee-filters"><span>Active filters:</span>{chips}</div>')
else:
    st.html('<div class="pee-filters">No additional filters applied.</div>')

# --- B. Evidence overview -----------------------------------------------------

section_heading(
    "2. Evidence overview",
    "Counts from the currently filtered synthetic dataset. They describe dataset coverage, "
    "not the strength or volume of real-world evidence.",
)
counts = du.summarise(filtered)
col1, col2, col3 = st.columns(3)
col1.metric("Projects represented", counts["projects"], border=True)
col2.metric("Findings", counts["findings"], border=True)
col3.metric("Thematic categories", counts["themes"], border=True)

if not filtered.empty:
    dist1, dist2 = st.columns(2)
    dist1.html(
        distribution_html("Findings by thematic category", filtered["thematic_category"].value_counts())
    )
    dist2.html(distribution_html("Findings by evidence type", filtered["evidence_type"].value_counts()))

# --- C. Findings explorer -----------------------------------------------------

section_heading(
    "3. Findings explorer",
    "Findings are shown as reported by the (synthetic) source. Interpretation remains with the reader.",
)

if filtered.empty:
    st.warning(
        "No findings match the current filters. Adjust the filters or select 'Reset filters'.",
        icon=":material/filter_alt_off:",
    )
else:
    tab_theme, tab_compare, tab_table, tab_projects = st.tabs(
        [
            ":material/view_agenda: Findings by theme",
            ":material/compare_arrows: Compare across projects",
            ":material/table_view: Table and export",
            ":material/folder_open: Projects",
        ]
    )

    with tab_theme:
        for theme, group in filtered.groupby("thematic_category", sort=True):
            n_projects = group["project_id"].nunique()
            cards = "".join(finding_card_html(row) for _, row in group.iterrows())
            st.html(
                '<div class="pee-theme-heading">'
                f'<span class="pee-theme-heading__title" role="heading" aria-level="3">{esc(theme)}</span>'
                f'<span class="pee-muted">{len(group)} findings from {n_projects} '
                f'project{"s" if n_projects != 1 else ""}</span></div>'
                f'<div class="pee-grid">{cards}</div>'
            )

    # FR-03: findings on one theme from different projects, side by side.
    with tab_compare:
        compare_options = sorted(filtered["thematic_category"].unique())
        if st.session_state.get("compare_theme") not in compare_options:
            st.session_state["compare_theme"] = compare_options[0]
        compare_theme = st.segmented_control(
            "Theme to compare", compare_options, key="compare_theme"
        ) or compare_options[0]
        st.caption(
            "Read findings from different projects side by side to identify consistent results, "
            "apparent tensions and gaps. Differences in method, location and scale may explain "
            "apparent disagreements."
        )

        theme_rows = filtered[filtered["thematic_category"] == compare_theme]
        panels = "".join(
            comparison_panel_html(group) for _, group in theme_rows.groupby("project_id", sort=True)
        )
        st.html(f'<div class="pee-grid">{panels}</div>')

        with st.expander("Show comparison as a table"):
            st.dataframe(
                theme_rows[
                    ["project_title", "finding_title", "evidence_type", "evidence_limitation", "source_reference"]
                ],
                column_config={
                    "project_title": "Project",
                    "finding_title": "Finding",
                    "evidence_type": "Evidence type",
                    "evidence_limitation": "Limitations / caveats",
                    "source_reference": "Source reference",
                },
                hide_index=True,
                width="stretch",
            )

        st.markdown("**Coverage: findings per theme and project**")
        st.html(coverage_matrix_html(du.theme_project_matrix(filtered), project_titles))
        st.caption(
            "Columns are synthetic project IDs (hover for the title, or see the Projects tab). "
            "A dash shows where a project in the current selection has no finding on a theme; "
            "this reflects dataset coverage only."
        )

    # FR-07: export of the filtered overview for offline review.
    with tab_table:
        table_columns = [
            "finding_id",
            "finding_title",
            "finding_description",
            "project_id",
            "project_title",
            "policy_topic",
            "thematic_category",
            "evidence_type",
            "evidence_limitation",
            "source_document",
            "source_reference",
        ]
        export = filtered[table_columns]
        st.dataframe(
            export,
            column_config={
                "finding_id": "Finding ID",
                "finding_title": "Finding",
                "finding_description": "Description",
                "project_id": "Project ID",
                "project_title": "Project",
                "policy_topic": "Policy topic",
                "thematic_category": "Theme",
                "evidence_type": "Evidence type",
                "evidence_limitation": "Limitations / caveats",
                "source_document": "Source document",
                "source_reference": "Source reference",
            },
            hide_index=True,
            width="stretch",
        )
        st.download_button(
            "Download filtered findings (CSV)",
            data=export.to_csv(index=False).encode("utf-8"),
            file_name="filtered_findings_synthetic.csv",
            mime="text/csv",
            icon=":material/download:",
        )

    with tab_projects:
        project_counts = filtered.groupby("project_id").size().rename("findings_in_view")
        project_view = (
            projects[projects["project_id"].isin(filtered["project_id"])]
            .drop_duplicates("project_id")
            .merge(project_counts, left_on="project_id", right_index=True)
        )
        cards = "".join(project_card_html(project) for _, project in project_view.iterrows())
        st.html(f'<div class="pee-grid">{cards}</div>')

# --- D. Source traceability (FR-04, DR-01) ------------------------------------

section_heading("4. Source traceability")
st.html(
    '<div class="pee-box pee-box--blue">'
    "Every finding shown is linked to a project, a source document and a source reference. "
    "Findings without these links are excluded from display. In this prototype all identifiers "
    "(<span class=\"pee-ref\">SYN-P...</span>, <span class=\"pee-ref\">SYN-F...</span>, "
    "<span class=\"pee-ref\">SYN-SRC-...</span>) and document titles are <strong>synthetic</strong>. "
    "A production service would need verified document-level references and working links to the "
    "original sources, such as project deliverables or publications.</div>"
)
if not filtered.empty:
    with st.expander("Source references for the current selection", icon=":material/link:"):
        st.dataframe(
            filtered[["finding_id", "project_id", "source_document", "source_reference"]],
            column_config={
                "finding_id": "Finding ID",
                "project_id": "Project ID",
                "source_document": "Source document",
                "source_reference": "Source reference",
            },
            hide_index=True,
            width="stretch",
        )

# --- E. Evidence limitations and human review (BR-02, FR-05) -----------------

section_heading("5. Evidence limitations and human review")
st.html(
    '<div class="pee-two-col">'
    '<div class="pee-box"><div class="pee-box__title">Limitations of this overview</div><ul>'
    "<li><strong>Coverage is incomplete and illustrative.</strong> The dataset is a small synthetic "
    "sample and does not represent the full body of research on any topic.</li>"
    "<li><strong>Findings require interpretation in context.</strong> Results depend on local "
    "conditions, methods and scale; agreement or tension between projects needs expert reading.</li>"
    "<li><strong>Verification is necessary.</strong> Sources must be checked and evidence quality "
    "assessed before a finding is used in policy work.</li>"
    "<li><strong>No policy judgement.</strong> The application organises reported findings. It does "
    "not assess policy options or produce policy recommendations.</li></ul></div>"
    '<div class="pee-box pee-box--blue"><div class="pee-box__title">Intended human review step</div><ol>'
    "<li>Review the filtered findings and their caveats.</li>"
    "<li>Open and verify the underlying source documents.</li>"
    "<li>Consult subject-matter colleagues where interpretation is uncertain.</li>"
    "<li>Decide what, if anything, is used in the briefing and how it is worded.</li></ol>"
    "<p style=\"margin:.6rem 0 0\">Responsibility for interpretation and drafting stays with the "
    "policy officer.</p></div></div>"
)

st.html(
    '<footer class="pee-footer"><strong>Policy Evidence Explorer</strong> &middot; '
    f"{esc(SYNTHETIC_NOTICE)}<br>All projects, findings and references are fictional and must not be "
    "cited as evidence.</footer>"
)
