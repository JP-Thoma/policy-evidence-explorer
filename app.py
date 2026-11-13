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
  border-bottom: 5px solid #ffd617; border-radius: 4px; }
.pee-masthead__eyebrow { font-size: .78rem; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; color: #c9d7f0; margin: 0 0 .4rem; }
.pee-masthead h1.pee-masthead__title { font-size: 2.1rem; font-weight: 700; line-height: 1.2;
  margin: 0; padding: 0; color: #ffffff; }
.pee-masthead__subtitle { font-size: 1.05rem; margin: .45rem 0 0; color: #e6ecf7; }

.pee-section { margin: 1.6rem 0 .6rem; }
.pee-section__title { font-size: 1.4rem; font-weight: 700; color: #262b38; padding-bottom: .45rem;
  border-bottom: 1px solid #d9e1f2; position: relative; }
.pee-section__title::after { content: ""; position: absolute; left: 0; bottom: -1px; width: 3rem;
  height: 3px; background: #ffd617; }
.pee-section__lead { color: #4a5568; margin: .55rem 0 0; font-size: .95rem; }

.st-key-topic_panel { background: #ffffff; border: 1px solid #d9e1f2; border-left: 4px solid #004494;
  border-radius: 4px; padding: 1rem 1.25rem 1.1rem; gap: .75rem; }
.pee-filters { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; font-size: .86rem;
  color: #4a5568; padding-top: .75rem; border-top: 1px solid #e6ecf7; }
.pee-filters__label { font-weight: 700; color: #262b38; margin-right: .35rem; }

.pee-tag { display: inline-block; font-size: .75rem; font-weight: 700; padding: .15rem .55rem;
  border-radius: 2px; background: #e6ecf7; color: #004494; }
.pee-tag--neutral { background: #eef0f3; color: #404b5a; }
.pee-tag--synthetic { background: #fff3b0; color: #5c4a00; }
.pee-muted { color: #6b7280; font-size: .85rem; }
.pee-ref { font-family: Consolas, "Courier New", monospace; font-size: .82rem; background: #f3f6fc;
  border: 1px solid #d9e1f2; padding: 0 .3rem; border-radius: 2px; color: #262b38; }

.pee-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: .9rem;
  align-items: start; }

.pee-panel { background: #ffffff; border: 1px solid #d9e1f2; border-top: 4px solid #004494;
  border-radius: 4px; padding: .9rem 1.1rem 1rem; color: #262b38; }
.pee-panel__project { font-weight: 700; font-size: 1rem; line-height: 1.35; }
.pee-panel__context { font-size: .82rem; color: #6b7280; margin-top: .15rem; }
.pee-panel__about { font-size: .85rem; color: #4a5568; line-height: 1.4; margin-top: .4rem; }
.pee-panel__item { padding-top: .8rem; margin-top: .8rem; border-top: 1px solid #d9e1f2; }
.pee-panel__finding { font-weight: 700; font-size: .95rem; line-height: 1.35; margin-bottom: .3rem; }
.pee-panel__desc { font-size: .9rem; line-height: 1.5; margin-bottom: .5rem; }
.pee-panel__meta { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; margin-bottom: .5rem; }
.pee-caveat { background: #fdf3e7; border-left: 3px solid #e57200; padding: .45rem .7rem;
  font-size: .85rem; line-height: 1.45; }
.pee-caveat__label { display: block; font-weight: 700; font-size: .7rem; text-transform: uppercase;
  letter-spacing: .06em; color: #8a4500; margin-bottom: .1rem; }
.pee-panel__source { font-size: .82rem; color: #4a5568; margin-top: .5rem; line-height: 1.5; }

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

.pee-footer { margin-top: 2.5rem; background: #004494; color: #e6ecf7; padding: 1.1rem 1.5rem;
  border-top: 5px solid #ffd617; font-size: .85rem; line-height: 1.5; display: flex; flex-wrap: wrap;
  justify-content: space-between; align-items: flex-end; gap: .75rem 2rem; }
.pee-footer strong { color: #ffffff; }
.pee-footer__author { white-space: nowrap; }
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


def comparison_panel_html(group: pd.DataFrame, description: str) -> str:
    """One project's findings on a theme: finding, caveat and source (FR-03 to FR-06)."""
    first = group.iloc[0]
    items = "".join(
        '<div class="pee-panel__item">'
        f'<div class="pee-panel__finding" role="heading" aria-level="4">{esc(r.finding_title)}</div>'
        f'<div class="pee-panel__desc">{esc(r.finding_description)}</div>'
        '<div class="pee-panel__meta">'
        f'<span class="pee-tag pee-tag--neutral">{esc(r.evidence_type)}</span>'
        '<span class="pee-tag pee-tag--synthetic">Synthetic</span></div>'
        '<div class="pee-caveat"><span class="pee-caveat__label">Limitations and caveats</span>'
        f"{esc(r.evidence_limitation)}</div>"
        f'<div class="pee-panel__source">Source: {esc(r.source_document)} '
        f'<span class="pee-ref">{esc(r.source_reference)}</span></div>'
        "</div>"
        for r in group.itertuples()
    )
    return (
        '<section class="pee-panel">'
        f'<div class="pee-panel__project" role="heading" aria-level="3">{esc(first["project_title"])}</div>'
        f'<div class="pee-panel__context">{esc(first["project_id"])} &middot; {esc(first["research_area"])}</div>'
        f'<div class="pee-panel__about">{esc(description)}</div>'
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


def plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


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

# --- A. Policy topic selection and filters (FR-08, FR-01, FR-02) -------------

section_heading("1. Policy Topic")

# Topic order follows the projects file; options come from the data, not the code.
available_topics = set(evidence["policy_topic"])
topics = [t for t in projects["policy_topic"].drop_duplicates() if t in available_topics]

topic_panel = st.container(key="topic_panel")
with topic_panel:
    topic = st.selectbox("Select the policy topic of your briefing", topics, key="topic", width=520)
topic_evidence = du.filter_findings(evidence, topic=topic)

project_titles = (
    topic_evidence.drop_duplicates("project_id").set_index("project_id")["project_title"].to_dict()
)

with st.sidebar:
    st.markdown("### Refine the Selection")
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
    filter_html = f'<span class="pee-filters__label">Active filters</span>{chips}'
else:
    filter_html = (
        '<span class="pee-filters__label">Active filters</span>'
        '<span>None. Refine by theme, project, evidence type or keyword in the sidebar.</span>'
    )
topic_panel.html(f'<div class="pee-filters">{filter_html}</div>')

# --- B. Evidence overview -----------------------------------------------------

section_heading(
    "2. Evidence Overview",
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
    "3. Findings Explorer",
    "Findings are shown as reported by the (synthetic) source. Interpretation remains with the reader.",
)

if filtered.empty:
    st.warning(
        "No findings match the current filters. Adjust the filters or select 'Reset filters'.",
        icon=":material/filter_alt_off:",
    )
else:
    tab_compare, tab_table = st.tabs(
        [":material/compare_arrows: Compare findings", ":material/table_view: Table and export"]
    )

    # FR-03: one foldable section per theme, with each project's findings side by side.
    with tab_compare:
        st.caption(
            "Each theme shows what different projects report, side by side, to help spot consistent "
            "results, apparent tensions and gaps. Select a theme to open or close it."
        )
        descriptions = projects.drop_duplicates("project_id").set_index("project_id")["short_description"]
        for i, (theme, group) in enumerate(filtered.groupby("thematic_category", sort=True)):
            n_projects = group["project_id"].nunique()
            label = f"**{theme}** \u2003{plural(len(group), 'finding')} from {plural(n_projects, 'project')}"
            with st.expander(label, expanded=i == 0):
                panels = "".join(
                    comparison_panel_html(project_rows, descriptions.get(pid, ""))
                    for pid, project_rows in group.groupby("project_id", sort=True)
                )
                st.html(f'<div class="pee-grid">{panels}</div>')

        with st.expander("Coverage overview: findings per theme and project", icon=":material/grid_on:"):
            st.html(coverage_matrix_html(du.theme_project_matrix(filtered), project_titles))
            st.caption(
                "Columns are synthetic project IDs (hover for the project title). A dash shows where a "
                "project in the current selection has no finding on a theme; this reflects dataset "
                "coverage only."
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

st.html(
    '<footer class="pee-footer"><div><strong>Policy Evidence Explorer</strong> &middot; '
    f"{esc(SYNTHETIC_NOTICE)}<br>All projects, findings and references are fictional and must not be "
    "cited as evidence.</div>"
    '<div class="pee-footer__author">Created by <strong>Jan Phillip Thoma</strong></div></footer>'
)
