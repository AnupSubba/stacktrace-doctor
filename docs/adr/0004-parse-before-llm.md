# ADR 0004: Parse stack traces with code before calling the LLM

- Status: Accepted
- Date: 2026-10-25

## Context
LLMs sometimes pick the top exception instead of the real cause, which is usually the deepest
"Caused by".

## Decision
A regex parser extracts the exception chain and deepest cause first. That summary drives
retrieval, and is given to the LLM ahead of the (truncated) raw trace.

## Alternatives
Send the raw trace straight to the LLM: simpler, less reliable, more tokens.

## Consequences
More code to maintain, but deterministic, unit-tested, cheaper and more accurate. Non-traces are
rejected without an LLM call.
