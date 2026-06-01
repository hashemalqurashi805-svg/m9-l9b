"""POST data/recipes_kg.ttl into the Fuseki `recipes` dataset.

Fully implemented — learners do not modify this file. Run after
`docker compose up` so the linker tests can hit a populated KG.
"""

import sys

import requests

FUSEKI_DATA_URL = "http://localhost:3030/recipes/data"
TTL_FILE = "data/recipes_kg.ttl"


def main():
    with open(TTL_FILE, "rb") as f:
        body = f.read()
    response = requests.post(
        FUSEKI_DATA_URL,
        data=body,
        headers={"Content-Type": "text/turtle"},
        timeout=30,
    )
    response.raise_for_status()
    print(f"Loaded {TTL_FILE} into {FUSEKI_DATA_URL} ({response.status_code})")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"load_dataset failed: {exc}", file=sys.stderr)
        sys.exit(1)
