"""Pydantic models shared by the parser, the chain and the UI."""

from typing import Literal

from pydantic import BaseModel, Field


class ExceptionInfo(BaseModel):
    type: str  # e.g. org.hibernate.LazyInitializationException
    message: str = ""

    @property
    def simple_name(self) -> str:
        return self.type.rsplit(".", 1)[-1]


class ParsedTrace(BaseModel):
    chain: list[ExceptionInfo]  # top exception first, deepest cause last
    frameworks: list[str]  # e.g. ["Spring Boot", "Hibernate"]

    @property
    def root(self) -> ExceptionInfo:
        return self.chain[-1]


class Diagnosis(BaseModel):
    root_cause: str = Field(description="One sentence: what actually went wrong")
    explanation: str = Field(description="Plain-English explanation, 2-4 sentences")
    fix_steps: list[str] = Field(description="Ordered steps to fix it")
    code_snippet: str | None = Field(default=None, description="Java, YAML or properties fix if relevant")
    confidence: Literal["high", "medium", "low"]
    sources: list[str] = Field(default_factory=list, description="URLs taken ONLY from the provided context")
