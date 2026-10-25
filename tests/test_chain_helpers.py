from langchain_core.documents import Document

from stacktrace_doctor.chain import format_chain, keep_known_sources
from stacktrace_doctor.models import Diagnosis, ExceptionInfo, ParsedTrace
from stacktrace_doctor.retriever import build_query

DOCS = [
    Document(page_content="a", metadata={"url": "https://docs.spring.io/a"}),
    Document(page_content="b", metadata={"url": "https://docs.spring.io/b"}),
]


def diagnosis(sources):
    return Diagnosis(root_cause="x", explanation="y", fix_steps=["z"], confidence="high", sources=sources)


def test_invented_urls_are_removed():
    d = keep_known_sources(diagnosis(["https://docs.spring.io/a", "https://made-up.example"]), DOCS)
    assert d.sources == ["https://docs.spring.io/a"]


def test_falls_back_to_retrieved_sources():
    d = keep_known_sources(diagnosis(["https://made-up.example"]), DOCS)
    assert d.sources == ["https://docs.spring.io/a", "https://docs.spring.io/b"]


def test_duplicate_sources_are_removed():
    d = keep_known_sources(diagnosis(["https://docs.spring.io/a", "https://docs.spring.io/a"]), DOCS)
    assert d.sources == ["https://docs.spring.io/a"]


PARSED = ParsedTrace(
    chain=[
        ExceptionInfo(type="org.springframework.beans.factory.UnsatisfiedDependencyException", message="top"),
        ExceptionInfo(type="org.springframework.beans.factory.NoSuchBeanDefinitionException", message="No bean"),
    ],
    frameworks=["Spring Framework"],
)


def test_query_puts_deepest_cause_first():
    q = build_query(PARSED)
    assert q.startswith("org.springframework.beans.factory.NoSuchBeanDefinitionException")
    assert "Spring Framework" in q


def test_chain_is_numbered_top_to_deepest():
    lines = format_chain(PARSED).splitlines()
    assert lines[0].startswith("1. org.springframework.beans.factory.UnsatisfiedDependencyException")
    assert lines[1].startswith("2. org.springframework.beans.factory.NoSuchBeanDefinitionException")
