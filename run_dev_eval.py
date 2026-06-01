"""Convenience: run the linker over data/dev.jsonl and print P/R/F1.

Fully implemented — learners do not modify. Useful for tuning
disambiguation against the dev split before the autograder runs against
the held-out test split.
"""

import json
import sys
from dataclasses import asdict

from linker.link import link
from linker.score import score


def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    docs = load_jsonl("data/dev.jsonl")
    predictions = []
    gold = []
    for doc in docs:
        results = link(doc["text"], doc["ner_spans"])
        for r in results:
            d = asdict(r) if hasattr(r, "__dataclass_fields__") else dict(r)
            predictions.append(
                {
                    "doc_id": doc["doc_id"],
                    "start": d["start"],
                    "end": d["end"],
                    "predicted_uri": d["predicted_uri"],
                }
            )
        for g in doc["gold"]:
            gold.append(
                {
                    "doc_id": doc["doc_id"],
                    "start": g["span_start"],
                    "end": g["span_end"],
                    "gold_uri": g["gold_uri"],
                }
            )
    metrics = score(predictions, gold)
    print(
        f"dev precision={metrics['precision']:.4f} "
        f"recall={metrics['recall']:.4f} "
        f"f1={metrics['f1']:.4f}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"run_dev_eval failed: {exc}", file=sys.stderr)
        sys.exit(1)
