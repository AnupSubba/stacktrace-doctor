# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.2.0] - 2026-10-25
### Added
- 24 knowledge cards for common Spring, JPA/Hibernate, Spring Security and core Java errors.
- Ingestion script that builds the Chroma index (optional official docs via `--docs`).
- Retriever and LLM chain: Groq primary, Gemini fallback, structured `Diagnosis` output.
- Source filter: URLs not present in retrieved documents are removed.

## [0.1.0] - 2026-10-25
### Added
- Project structure, pre-commit hooks and GitLab CI pipeline.
- Requirements, ADRs 0001–0004 and data-source notes.
- Configuration, Pydantic models and the rule-based stack trace parser with tests.
