# ADR 0003: Groq as primary LLM, Gemini as fallback, temperature 0

- Status: Accepted
- Date: 2026-10-25

## Context
Free tiers have rate limits and occasional outages.

## Decision
Call Groq first; if it fails, fall back to Gemini. Use temperature 0 for repeatable answers.
Model names are configuration (environment variables), not code.

## Consequences
More reliable on free tiers. Two API keys to manage. When a provider retires a model, only the
secret changes.
