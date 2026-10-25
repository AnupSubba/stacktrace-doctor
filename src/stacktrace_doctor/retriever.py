"""Loads the committed Chroma index and returns the most relevant documents."""

from functools import lru_cache

from langchain_core.documents import Document

from . import config
from .models import ParsedTrace


class IndexMissingError(RuntimeError):
    """Raised when data/chroma/ has not been built yet."""


@lru_cache
def get_retriever():
    if not config.CHROMA_DIR.exists():
        raise IndexMissingError("Vector index not found. Run: uv run python scripts/ingest.py")
    # Imported here so the parser and tests don't need the embedding model.
    from langchain_chroma import Chroma
    from langchain_community.embeddings import FastEmbedEmbeddings

    embeddings = FastEmbedEmbeddings(model_name=config.EMBED_MODEL)
    store = Chroma(
        persist_directory=str(config.CHROMA_DIR),
        collection_name=config.COLLECTION,
        embedding_function=embeddings,
    )
    return store.as_retriever(search_kwargs={"k": config.TOP_K})


def build_query(parsed: ParsedTrace) -> str:
    """The deepest cause matters most; the top exception and frameworks add context."""
    root = parsed.root
    parts = [root.type, root.simple_name, root.message]
    if len(parsed.chain) > 1:
        parts.append(parsed.chain[0].simple_name)
    parts.extend(parsed.frameworks)
    return " ".join(p for p in parts if p)


def retrieve(parsed: ParsedTrace) -> list[Document]:
    return get_retriever().invoke(build_query(parsed))
