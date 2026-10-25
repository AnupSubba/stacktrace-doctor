# ADR 0001: Use fastembed instead of sentence-transformers

- Status: Accepted
- Date: 2026-10-25

## Context
The app must run on free hosting with limited memory. sentence-transformers pulls in PyTorch,
which is large and slow to install.

## Decision
Use fastembed (ONNX runtime) with the small `BAAI/bge-small-en-v1.5` model.

## Alternatives
sentence-transformers (heavier); a hosted embedding API (adds cost, latency and another key).

## Consequences
Small install, CPU-only, no extra API. Slightly lower quality than large models, which is fine
for a focused document set.
