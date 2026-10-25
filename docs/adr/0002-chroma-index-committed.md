# ADR 0002: Build the ChromaDB index offline and commit it

- Status: Accepted
- Date: 2026-10-25

## Context
The app needs a vector index at start-up but should not depend on an external database.

## Decision
`scripts/ingest.py` builds the index into `data/chroma/` locally; the folder is committed.

## Alternatives
A hosted vector database (Pinecone, Chroma Cloud): more moving parts and accounts.

## Consequences
Reproducible and instant start-up. The index must stay small (well under 100 MB) and be rebuilt
when knowledge cards change.
