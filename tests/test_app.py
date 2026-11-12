"""Smoke tests for the Streamlit app using Streamlit's built-in AppTest."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parents[1] / "app.py")


def _run_app() -> AppTest:
    return AppTest.from_file(APP_PATH, default_timeout=30).run()


def _metrics(at: AppTest) -> list[str]:
    return [m.value for m in at.metric]


def _html(at: AppTest) -> str:
    return " ".join(el.proto.body for el in at.get("html"))


def test_app_loads_with_title_and_notice():
    at = _run_app()
    assert not at.exception
    page = _html(at)
    assert "Policy Evidence Explorer" in page
    assert "Illustrative proof of concept using synthetic research data." in page
    assert "Not an official European Commission service." in page
    assert at.selectbox(key="topic").value == "Urban climate adaptation"
    assert _metrics(at) == ["8", "19", "4"]


def test_second_topic_updates_counts_and_findings():
    at = _run_app()
    at.selectbox(key="topic").select("Sustainable urban mobility").run()
    assert not at.exception
    assert _metrics(at) == ["6", "15", "4"]
    page = _html(at)
    assert "SYN-F020" in page
    assert "SYN-F001" not in page


def test_theme_filter_updates_counts_and_reset_restores_them():
    at = _run_app()
    at.multiselect(key="themes").select("Flood resilience").run()
    assert not at.exception
    assert _metrics(at) == ["4", "5", "1"]

    at.button(key="reset_filters").click().run()
    assert _metrics(at) == ["8", "19", "4"]


def test_switching_topic_drops_filters_that_no_longer_apply():
    at = _run_app()
    at.multiselect(key="themes").select("Flood resilience").run()
    at.selectbox(key="topic").select("Sustainable urban mobility").run()
    assert not at.exception
    assert at.multiselect(key="themes").value == []
    assert _metrics(at) == ["6", "15", "4"]


def test_empty_filter_result_shows_warning():
    at = _run_app()
    at.text_input(key="keyword").input("no such keyword xyz").run()
    assert not at.exception
    assert _metrics(at) == ["0", "0", "0"]
    assert any("No findings match" in w.value for w in at.warning)
