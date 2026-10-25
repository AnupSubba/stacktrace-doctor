"""UI smoke tests with Streamlit's AppTest. No LLM or index needed."""

from streamlit.testing.v1 import AppTest


def run_app() -> AppTest:
    return AppTest.from_file("../app.py", default_timeout=30).run()


def test_page_loads_with_samples():
    at = run_app()
    assert not at.exception
    assert at.title[0].value.endswith("StackTrace Doctor")
    assert len(at.selectbox[0].options) > 1  # "—" plus the samples


def test_non_trace_input_shows_warning_without_calling_llm():
    at = run_app()
    at.text_area[0].input("hello world").run()
    at.button[0].click().run()
    assert at.warning, "expected a friendly warning for input that isn't a stack trace"
    assert at.session_state.count == 0


def test_too_long_input_is_rejected():
    at = run_app()
    at.text_area[0].input("java.lang.RuntimeException: " + "x" * 25_000).run()
    at.button[0].click().run()
    assert at.error
