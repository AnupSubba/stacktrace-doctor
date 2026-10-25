"""Score StackTrace Doctor against the evaluation set with LangSmith.

    uv run python evals/run_eval.py

Needs the LLM keys and LANGSMITH_API_KEY in .env, and the index in data/chroma/.
Each evaluation run makes one LLM call per trace.
"""

import csv
from pathlib import Path

from langsmith import Client, evaluate

from stacktrace_doctor.chain import diagnose
from stacktrace_doctor.parser import parse

HERE = Path(__file__).parent
DATASET = "stacktrace-doctor-eval"


def ensure_dataset(client: Client) -> None:
    if client.has_dataset(dataset_name=DATASET):
        return
    rows = list(csv.DictReader((HERE / "expected.csv").open(encoding="utf-8")))
    ds = client.create_dataset(DATASET, description="Real Java/Spring stack traces with known causes")
    client.create_examples(
        dataset_id=ds.id,
        inputs=[{"trace": (HERE / "traces" / r["file"]).read_text(encoding="utf-8")} for r in rows],
        outputs=[{"root_cause": r["root_cause"], "key_fix": r["key_fix"]} for r in rows],
    )


def target(inputs: dict) -> dict:
    trace = inputs["trace"]
    return diagnose(trace, parse(trace)).model_dump()


def _answer_text(outputs: dict) -> str:
    return " ".join([outputs["root_cause"], outputs["explanation"], *outputs["fix_steps"]]).lower()


def mentions_root_cause(outputs: dict, reference_outputs: dict) -> bool:
    """Simple first version: the expected key phrase appears in the answer."""
    return reference_outputs["root_cause"].lower() in _answer_text(outputs)


def mentions_key_fix(outputs: dict, reference_outputs: dict) -> bool:
    return reference_outputs["key_fix"].lower() in (
        _answer_text(outputs) + " " + (outputs.get("code_snippet") or "").lower()
    )


if __name__ == "__main__":
    client = Client()
    ensure_dataset(client)
    evaluate(
        target,
        data=DATASET,
        evaluators=[mentions_root_cause, mentions_key_fix],
        experiment_prefix="v1",
        max_concurrency=1,  # gentle on free-tier rate limits
    )
