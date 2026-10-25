"""Settings, read from environment variables.

Locally they come from a .env file. On Streamlit Community Cloud, root-level entries in the
app's Secrets settings are exposed as environment variables, so no code change is needed.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]

GROQ_MODEL = os.getenv("GROQ_MODEL", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "").strip()

CHROMA_DIR = Path(os.getenv("CHROMA_DIR", ROOT / "data" / "chroma"))
COLLECTION = "docs"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

MAX_INPUT_CHARS = 20_000
MAX_TRACE_CHARS_FOR_LLM = 4_000
TOP_K = 5
SESSION_LIMIT = 10


class ConfigError(RuntimeError):
    """Raised when a required setting is missing."""


def require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigError(f"Missing setting {name}. Add it to .env (local) or the app's secrets (cloud).")
    return value
