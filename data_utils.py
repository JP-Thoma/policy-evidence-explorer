"""Data loading, validation and filtering for the Policy Evidence Explorer.

Kept separate from app.py so the logic can be tested without Streamlit.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
PROJECTS_FILE = DATA_DIR / "projects.csv"
FINDINGS_FILE = DATA_DIR / "findings.csv"

PROJECT_COLUMNS = [
    "project_id",
    "project_title",
    "policy_topic",
    "short_description",
    "research_area",
]

FINDING_COLUMNS = [
    "finding_id",
    "project_id",
    "finding_title",
    "finding_description",
    "policy_topic",
    "thematic_category",
    "evidence_type",
    "evidence_limitation",
    "source_document",
    "source_reference",
]

# Fields a finding must have to be displayed (REQ DR-01: traceability).
TRACEABILITY_COLUMNS = ["project_id", "finding_title", "source_document", "source_reference"]

KEYWORD_SEARCH_COLUMNS = ["finding_title", "finding_description", "evidence_limitation"]


def _read_csv(path: Path | str, required_columns: list[str]) -> pd.DataFrame:
    """Read a CSV as text, strip whitespace and check that required columns exist."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"{path.name} is empty.") from exc

    df.columns = [str(col).strip() for col in df.columns]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"{path.name} is missing required columns: {', '.join(missing)}")

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def load_projects(path: Path | str = PROJECTS_FILE) -> pd.DataFrame:
    return _read_csv(path, PROJECT_COLUMNS)


def load_findings(path: Path | str = FINDINGS_FILE) -> pd.DataFrame:
    return _read_csv(path, FINDING_COLUMNS)


def validate_data(projects: pd.DataFrame, findings: pd.DataFrame) -> list[str]:
    """Return human-readable data quality issues (REQ DR-02). Empty list means no issues found."""
    issues: list[str] = []

    duplicate_projects = projects.loc[projects["project_id"].duplicated(), "project_id"].unique()
    if len(duplicate_projects):
        issues.append(f"Duplicate project IDs: {', '.join(duplicate_projects)}")

    duplicate_findings = findings.loc[findings["finding_id"].duplicated(), "finding_id"].unique()
    if len(duplicate_findings):
        issues.append(f"Duplicate finding IDs: {', '.join(duplicate_findings)}")

    orphan = findings.loc[~findings["project_id"].isin(projects["project_id"]), "finding_id"]
    if len(orphan):
        issues.append(f"Findings linked to an unknown project: {', '.join(orphan)}")

    for col in TRACEABILITY_COLUMNS:
        empty = findings.loc[findings[col] == "", "finding_id"]
        if len(empty):
            issues.append(f"Findings with empty '{col}': {', '.join(empty)}")

    return issues


def prepare_evidence(findings: pd.DataFrame, projects: pd.DataFrame) -> pd.DataFrame:
    """Join findings to projects and keep only findings that are fully traceable.

    Findings with an unknown project, a missing source reference or a duplicate ID
    are excluded so that every displayed finding can be traced to its source.
    """
    project_info = projects.drop_duplicates("project_id")[["project_id", "project_title", "research_area"]]
    evidence = findings.drop_duplicates("finding_id").merge(project_info, on="project_id", how="inner")

    traceable = (evidence[TRACEABILITY_COLUMNS] != "").all(axis=1)
    evidence = evidence.loc[traceable]

    return evidence.sort_values(["thematic_category", "project_id", "finding_id"]).reset_index(drop=True)


def filter_findings(
    evidence: pd.DataFrame,
    topic: str | None = None,
    themes: Iterable[str] | None = None,
    project_ids: Iterable[str] | None = None,
    evidence_types: Iterable[str] | None = None,
    keyword: str | None = None,
) -> pd.DataFrame:
    """Filter findings. A filter that is None or empty is not applied."""
    mask = pd.Series(True, index=evidence.index)

    if topic:
        mask &= evidence["policy_topic"] == topic
    if themes:
        mask &= evidence["thematic_category"].isin(list(themes))
    if project_ids:
        mask &= evidence["project_id"].isin(list(project_ids))
    if evidence_types:
        mask &= evidence["evidence_type"].isin(list(evidence_types))
    if keyword and keyword.strip():
        term = keyword.strip().lower()
        text_match = pd.Series(False, index=evidence.index)
        for col in KEYWORD_SEARCH_COLUMNS:
            text_match |= evidence[col].str.lower().str.contains(term, regex=False)
        mask &= text_match

    return evidence.loc[mask].reset_index(drop=True)


def summarise(evidence: pd.DataFrame) -> dict[str, int]:
    """Counts shown in the evidence overview."""
    return {
        "projects": int(evidence["project_id"].nunique()),
        "findings": int(len(evidence)),
        "themes": int(evidence["thematic_category"].nunique()),
    }


def theme_project_matrix(evidence: pd.DataFrame) -> pd.DataFrame:
    """Number of findings per theme (rows) and project (columns)."""
    if evidence.empty:
        return pd.DataFrame()
    return pd.crosstab(evidence["thematic_category"], evidence["project_id"])
