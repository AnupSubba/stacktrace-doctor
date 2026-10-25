"""Build the vector index in data/chroma/ from knowledge cards (and optional official docs).

Run locally whenever the cards change, then commit data/chroma/:

    uv run python scripts/ingest.py
    uv run python scripts/ingest.py --docs ../_docs/spring-boot=https://docs.spring.io/spring-boot/

--docs takes FOLDER=BASE_URL pairs; every .adoc/.md file under FOLDER is indexed with BASE_URL as its source.
"""

import argparse
import shutil
import sys
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stacktrace_doctor import config  # noqa: E402


def read_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Split a Markdown card into its front-matter fields and body."""
    if not text.startswith("---"):
        return {}, text
    _, header, body = text.split("---", 2)
    fields = {}
    for line in header.strip().splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, body.strip()


def load_cards(folder: Path) -> list[Document]:
    docs = []
    for path in sorted(folder.glob("*.md")):
        meta, body = read_front_matter(path.read_text(encoding="utf-8"))
        title = meta.get("title", path.stem)
        content = f"# {title}\nException: {meta.get('error', '')}\nFrameworks: {meta.get('frameworks', '')}\n\n{body}"
        docs.append(
            Document(
                page_content=content,
                metadata={"url": meta.get("source", ""), "title": title, "file": path.name, "kind": "card"},
            )
        )
    return docs


def load_docs(folder: Path, base_url: str) -> list[Document]:
    docs = []
    for path in sorted([*folder.rglob("*.adoc"), *folder.rglob("*.md")]):
        docs.append(
            Document(
                page_content=path.read_text(encoding="utf-8", errors="ignore"),
                metadata={"url": base_url, "title": path.stem, "file": path.name, "kind": "doc"},
            )
        )
    return docs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--docs", nargs="*", default=[], metavar="FOLDER=BASE_URL")
    args = parser.parse_args()

    cards = load_cards(ROOT / "knowledge")
    docs: list[Document] = []
    for pair in args.docs:
        folder, _, url = pair.partition("=")
        if not Path(folder).is_dir():
            sys.exit(f"Docs folder not found: {folder}")
        docs += load_docs(Path(folder), url)

    # Cards are short: keep each one whole. Long docs are split on AsciiDoc/Markdown headings.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000, chunk_overlap=400, separators=["\n== ", "\n=== ", "\n## ", "\n\n", "\n"]
    )
    chunks = cards + splitter.split_documents(docs)

    if config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)  # rebuild from scratch so deleted cards disappear
    embeddings = FastEmbedEmbeddings(model_name=config.EMBED_MODEL)
    Chroma.from_documents(
        chunks, embeddings, persist_directory=str(config.CHROMA_DIR), collection_name=config.COLLECTION
    )
    print(f"{len(cards)} cards + {len(docs)} doc files -> {len(chunks)} chunks in {config.CHROMA_DIR}")


if __name__ == "__main__":
    main()
