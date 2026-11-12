"""Basic data and filtering tests for the Policy Evidence Explorer."""

from pathlib import Path

import pandas as pd
import pytest

import data_utils as du


@pytest.fixture(scope="module")
def projects() -> pd.DataFrame:
    return du.load_projects()


@pytest.fixture(scope="module")
def findings() -> pd.DataFrame:
    return du.load_findings()


@pytest.fixture(scope="module")
def evidence(findings, projects) -> pd.DataFrame:
    return du.prepare_evidence(findings, projects)


# --- Dataset checks -----------------------------------------------------------


def test_expected_columns(projects, findings):
    assert set(du.PROJECT_COLUMNS) <= set(projects.columns)
    assert set(du.FINDING_COLUMNS) <= set(findings.columns)


def test_unique_ids(projects, findings):
    assert projects["project_id"].is_unique
    assert findings["finding_id"].is_unique


def test_findings_reference_existing_projects(projects, findings):
    assert findings["project_id"].isin(projects["project_id"]).all()


def test_source_references_not_empty(findings):
    assert (findings["source_reference"] != "").all()
    assert (findings["source_document"] != "").all()


def test_dataset_is_labelled_synthetic(projects, findings):
    assert projects["project_id"].str.startswith("SYN-").all()
    assert findings["finding_id"].str.startswith("SYN-").all()
    assert findings["source_reference"].str.startswith("SYN-SRC-").all()


def test_shipped_data_has_no_quality_issues(projects, findings, evidence):
    assert du.validate_data(projects, findings) == []
    assert len(evidence) == len(findings)


# --- Filtering ----------------------------------------------------------------


def test_topic_filter(evidence):
    climate = du.filter_findings(evidence, topic="Urban climate adaptation")
    mobility = du.filter_findings(evidence, topic="Sustainable urban mobility")
    assert (climate["policy_topic"] == "Urban climate adaptation").all()
    assert (mobility["policy_topic"] == "Sustainable urban mobility").all()
    assert len(climate) + len(mobility) == len(evidence)
    assert not set(climate["project_id"]) & set(mobility["project_id"])


def test_finding_topic_matches_project_topic(evidence, projects):
    project_topics = projects.set_index("project_id")["policy_topic"]
    assert (evidence["policy_topic"] == evidence["project_id"].map(project_topics)).all()


def test_theme_filter(evidence):
    result = du.filter_findings(evidence, themes=["Flood resilience"])
    assert not result.empty
    assert (result["thematic_category"] == "Flood resilience").all()


def test_combined_filters_and_counts(evidence):
    result = du.filter_findings(
        evidence, themes=["Urban heat mitigation"], project_ids=["SYN-P01", "SYN-P04"]
    )
    assert set(result["project_id"]) == {"SYN-P01", "SYN-P04"}
    assert du.summarise(result) == {"projects": 2, "findings": len(result), "themes": 1}


def test_findings_keep_project_link(evidence, projects):
    titles = projects.set_index("project_id")["project_title"]
    for _, row in evidence.iterrows():
        assert row["project_title"] == titles[row["project_id"]]


def test_keyword_filter_is_case_insensitive(evidence):
    result = du.filter_findings(evidence, keyword="GREEN ROOF")
    assert not result.empty
    assert (result["project_id"] == "SYN-P02").all()


def test_empty_result_is_handled(evidence):
    result = du.filter_findings(evidence, topic="Topic that does not exist")
    assert result.empty
    assert du.summarise(result) == {"projects": 0, "findings": 0, "themes": 0}
    assert du.theme_project_matrix(result).empty


def test_empty_filters_are_ignored(evidence):
    assert len(du.filter_findings(evidence, themes=[], project_ids=[], keyword="  ")) == len(evidence)


# --- Requirements catalogue ---------------------------------------------------


def test_requirements_catalogue_is_well_formed():
    path = Path(du.__file__).resolve().parent / "requirements" / "requirements.csv"
    reqs = pd.read_csv(path, dtype=str, keep_default_na=False)
    assert list(reqs.columns) == [
        "requirement_id",
        "category",
        "user_need",
        "requirement_description",
        "priority",
        "acceptance_criterion",
        "validation_status",
        "prototype_coverage",
    ]
    assert reqs["requirement_id"].is_unique
    assert set(reqs["category"]) <= {"Business", "Functional", "Data", "Non-functional"}
    assert set(reqs["priority"]) <= {"Must", "Should", "Could", "Won't for this pilot"}
    assert (reqs[reqs.columns] != "").all().all()


# --- Defensive handling -------------------------------------------------------


def test_missing_column_raises(tmp_path: Path):
    bad = tmp_path / "projects.csv"
    bad.write_text("project_id,project_title\nSYN-P99,Test\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns"):
        du.load_projects(bad)


def test_untraceable_findings_are_excluded(projects, findings):
    broken = findings.copy()
    broken.loc[0, "project_id"] = "SYN-P99"
    broken.loc[1, "source_reference"] = ""
    issues = du.validate_data(projects, broken)
    assert any("unknown project" in issue for issue in issues)
    assert any("source_reference" in issue for issue in issues)

    evidence = du.prepare_evidence(broken, projects)
    assert len(evidence) == len(findings) - 2
    assert (evidence["source_reference"] != "").all()
