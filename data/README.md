# data/

`chroma/` holds the vector index built by `scripts/ingest.py`. It is committed on purpose
(see docs/adr/0002) so the hosted app starts instantly without a database.

Rebuild it whenever you add or change a knowledge card:

    uv run python scripts/ingest.py
