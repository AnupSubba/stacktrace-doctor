"""StackTrace Doctor: Streamlit UI.

Run locally:  uv run streamlit run app.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))  # works even if the package isn't installed (e.g. on the host)

import streamlit as st  # noqa: E402

from stacktrace_doctor import __version__, config  # noqa: E402
from stacktrace_doctor.config import ConfigError  # noqa: E402
from stacktrace_doctor.parser import parse  # noqa: E402
from stacktrace_doctor.retriever import IndexMissingError  # noqa: E402

st.set_page_config(page_title="StackTrace Doctor", layout="centered")

CONFIDENCE = {"high": "🟢 High", "medium": "🟡 Medium", "low": "🔴 Low — please verify"}


@st.cache_data(show_spinner=False, ttl=86_400, max_entries=500)
def cached_diagnosis(text: str) -> dict:
    from stacktrace_doctor.chain import diagnose  # heavy imports only when needed

    return diagnose(text, parse(text)).model_dump()


def load_samples() -> dict[str, str]:
    return {
        p.stem.split("-", 1)[-1].replace("-", " ").capitalize(): p.read_text(encoding="utf-8")
        for p in sorted((ROOT / "samples").glob("*.txt"))
    }


def show(d: dict) -> None:
    st.subheader("Root cause")
    st.markdown(f"**{d['root_cause']}**")
    st.caption(f"Confidence: {CONFIDENCE.get(d['confidence'], d['confidence'])}")
    st.write(d["explanation"])

    st.subheader("How to fix it")
    st.markdown("\n".join(f"{i}. {step}" for i, step in enumerate(d["fix_steps"], 1)))
    if d.get("code_snippet"):
        language = "yaml" if ":" in d["code_snippet"] and "{" not in d["code_snippet"] else "java"
        st.code(d["code_snippet"], language=language)

    if d["sources"]:
        st.subheader("Sources")
        st.markdown("\n".join(f"- [{url}]({url})" for url in d["sources"]))


st.title("🩺 StackTrace Doctor")
st.write("Paste a Java / Spring Boot stack trace. Get the root cause, a fix and the docs.")
st.caption("Please remove passwords, tokens and customer data from logs before pasting.")

samples = load_samples()
pick = st.selectbox("Or try a sample", ["—", *samples])
trace = st.text_area("Stack trace", value=samples.get(pick, ""), height=280, placeholder="Paste the trace here…")

st.session_state.setdefault("count", 0)

if st.button("Diagnose", type="primary", use_container_width=True):
    parsed = parse(trace) if trace.strip() else None
    if len(trace) > config.MAX_INPUT_CHARS:
        st.error("That's very long. Paste just the exception and its 'Caused by' lines.")
    elif parsed is None:
        st.warning("I couldn't find a Java exception in that text. Paste the lines starting with the exception name.")
    elif st.session_state.count >= config.SESSION_LIMIT:
        st.info("Demo limit reached for this session. Please come back later.")
    else:
        with st.expander(f"Exception chain found ({len(parsed.chain)})", expanded=False):
            for i, e in enumerate(parsed.chain, 1):
                st.markdown(f"{i}. `{e.type}` {e.message}")
            st.caption("Frameworks: " + (", ".join(parsed.frameworks) or "none detected"))
        try:
            with st.spinner("Reading the trace and checking the docs…"):
                result = cached_diagnosis(trace)
            st.session_state.count += 1
            show(result)
        except (ConfigError, IndexMissingError) as err:
            st.error(f"Setup problem: {err}")
        except Exception:  # keep the page usable if a provider fails
            st.error("Something went wrong while contacting the AI service. Please try again in a minute.")

with st.sidebar:
    st.markdown("### About")
    st.write(
        "A rule-based parser finds the real root cause (the deepest *Caused by*), then an LLM explains it "
        "using only retrieved documentation, so every answer links to its sources."
    )
    st.caption(f"Version {__version__} · Not a substitute for reading the docs.")
