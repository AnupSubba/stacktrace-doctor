"""Prompt + LLM (Groq primary, Gemini fallback) with structured output."""

from functools import lru_cache

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from . import config
from .models import Diagnosis, ParsedTrace
from .retriever import retrieve

SYSTEM = (
    "You are a senior Java and Spring engineer helping a developer understand a stack trace. "
    "Diagnose the error using ONLY the context documents. The deepest cause in the exception chain "
    "is usually the real problem. Write in plain English. Only cite URLs that appear in the context. "
    "If the context does not cover this error, say so in the explanation and set confidence to 'low'. "
    "Never invent APIs, annotations or configuration properties."
)

HUMAN = (
    "Exception chain (top exception first, deepest cause last):\n{chain}\n\n"
    "Frameworks detected: {frameworks}\n\n"
    "Raw stack trace (truncated):\n{trace}\n\n"
    "Context documents:\n{context}"
)

PROMPT = ChatPromptTemplate.from_messages([("system", SYSTEM), ("human", HUMAN)])


@lru_cache
def build_llm():
    """Groq first; Gemini as fallback when a Google key is configured."""
    from langchain_groq import ChatGroq

    config.require("GROQ_API_KEY")
    primary = ChatGroq(model=config.require("GROQ_MODEL"), temperature=0).with_structured_output(Diagnosis)

    if not config.GEMINI_MODEL:
        return primary
    from langchain_google_genai import ChatGoogleGenerativeAI

    config.require("GOOGLE_API_KEY")
    fallback = ChatGoogleGenerativeAI(model=config.GEMINI_MODEL, temperature=0).with_structured_output(Diagnosis)
    return primary.with_fallbacks([fallback])


def format_context(docs: list[Document]) -> str:
    return "\n\n---\n\n".join(f"[Source: {d.metadata.get('url', '')}]\n{d.page_content}" for d in docs)


def format_chain(parsed: ParsedTrace) -> str:
    return "\n".join(f"{i}. {e.type}: {e.message}" for i, e in enumerate(parsed.chain, 1))


def keep_known_sources(diagnosis: Diagnosis, docs: list[Document]) -> Diagnosis:
    """Drop any URL the model returned that wasn't in the retrieved documents (US3)."""
    known = [d.metadata.get("url", "") for d in docs if d.metadata.get("url")]
    kept = [u for u in diagnosis.sources if u in known]
    if not kept:  # fall back to the retrieved sources themselves, in ranking order
        kept = list(dict.fromkeys(known))[:3]
    diagnosis.sources = list(dict.fromkeys(kept))[:5]
    return diagnosis


def diagnose(trace: str, parsed: ParsedTrace) -> Diagnosis:
    docs = retrieve(parsed)
    result = (PROMPT | build_llm()).invoke(
        {
            "chain": format_chain(parsed),
            "frameworks": ", ".join(parsed.frameworks) or "none detected",
            "trace": trace[: config.MAX_TRACE_CHARS_FOR_LLM],
            "context": format_context(docs),
        }
    )
    return keep_known_sources(result, docs)
