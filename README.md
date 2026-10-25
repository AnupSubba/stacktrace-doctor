# 🩺 StackTrace Doctor

**Paste a Java / Spring Boot stack trace. Get the root cause in plain English, a fix, and links to the official docs.**

Free, no sign-up. Live demo: _add your link after deployment_

## Why I built it

After 12+ years of Java and Spring work, I've seen how much time goes into decoding long stack traces where the real
problem is buried several "Caused by" levels deep. General chatbots answer confidently but without sources.
StackTrace Doctor finds the real cause with plain code first, then explains it using only retrieved documentation.

## How it works

```
Stack trace ──▶ Parser (plain Python) ──▶ Retriever (Chroma + fastembed) ──▶ LLM (Groq, Gemini fallback) ──▶ Diagnosis
                 deepest "Caused by"        knowledge cards + docs              answers ONLY from context      cause · fix · sources
```

1. **Parser** (`parser.py`): regex-based, no AI. Extracts the exception chain and the deepest cause, which is usually
   the real problem. Non-traces are rejected without calling the LLM.
2. **Retriever** (`retriever.py`): searches a local Chroma index of knowledge cards (and optional official docs).
3. **LLM chain** (`chain.py`): returns a validated Pydantic `Diagnosis`. Any source URL the model returns that wasn't
   in the retrieved documents is removed in code.

Design decisions are recorded in [`docs/adr/`](docs/adr).

## Results

| Metric | Value |
|--------|-------|
| Evaluation set | 10 traces (growing to 30 from the "error zoo") |
| Root-cause accuracy | _run `evals/run_eval.py` and record it here_ |
| Knowledge cards | 24 |

## Quick start

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync                                   # install dependencies
cp .env.example .env                      # then add your Groq / Gemini / LangSmith keys
uv run python scripts/ingest.py           # build the vector index in data/chroma/
uv run streamlit run app.py               # open http://localhost:8501
```

## Development

```bash
uv run pre-commit install                 # lint + secret scan on every commit
uv run pytest                             # tests (no API keys needed)
uv run ruff check . && uv run ruff format --check .
uv run python evals/run_eval.py           # LangSmith evaluation (uses your API keys)
```

After changing dependencies, regenerate `requirements.txt` (used by the hosting platform):

```bash
uv export --format requirements-txt --no-hashes --no-dev --no-header > requirements.txt
```

### Git workflow

- `main` is protected; every change goes through a merge request with a passing pipeline.
- Branch names: `feat/…`, `fix/…`, `docs/…`, `chore/…`. Commits follow
  [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`).
- Versions follow [Semantic Versioning](https://semver.org/); every release is a Git tag (`v0.3.0`) with notes in
  [CHANGELOG.md](CHANGELOG.md).

## Project structure

```
src/stacktrace_doctor/   config, models, parser, retriever, chain
app.py                   Streamlit UI
scripts/ingest.py        builds the vector index
knowledge/               knowledge cards (one per common error)
samples/                 sample traces shown in the UI
evals/                   evaluation traces, expected answers, LangSmith script
tests/                   pytest suite (parser, chain helpers, UI smoke tests)
docs/                    requirements, ADRs, data sources
```

## Data and licences

Knowledge cards are original work and link to the official Spring, Hibernate, HikariCP and Java documentation.
See [`docs/data-sources.md`](docs/data-sources.md). Links were written without live checking — please report broken ones.

## Limitations

- Focused on Spring Boot, Spring Data/Hibernate, Spring Security and core Java errors.
- Answers can be wrong: always check the linked docs. Low-confidence answers are marked.
- Remove secrets and customer data from logs before pasting.
- The free hosting tier sleeps when idle; the first visit may take a moment to wake up.

## Roadmap

More frameworks (Kafka, Redis, Feign, Spring Cloud), log-file upload, an MCP server so IDEs and Claude Desktop can call
it, and "helpful / not helpful" feedback to grow the evaluation set.

## Licence

[MIT](LICENSE) © 2026 Anup Kumar Subba
