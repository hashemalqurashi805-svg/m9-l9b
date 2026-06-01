# Lab 9B Data

## Files

- `recipes_kg.ttl` — Pre-built knowledge graph (~250 triples). Cuisines with `rdfs:subClassOf` hierarchy, ingredients with SKOS pref/alt labels, authors, and 30 recipe instances with `:cuisine`, `:primaryIngredient`, `:authoredBy`, `:popularityScore`. Do not modify — the autograder loads this exact TTL into Fuseki.
- `train.jsonl` — 140 annotated docs. You may inspect these for design intuition.
- `dev.jsonl` — 30 annotated docs. Use these for local tuning (run `python run_dev_eval.py`).
- `test.jsonl` — 30 annotated docs. The autograder reports test-split P/R/F1 against threshold gates.

## JSONL Schema

Each line in `train/dev/test.jsonl` is a JSON object:

```json
{
  "doc_id": "train-0012",
  "text": "A classic italian dish: eggplant sauteed with basil.",
  "ner_spans": [
    {"text": "italian",  "label": "NORP",    "start": 10, "end": 17},
    {"text": "eggplant", "label": "PRODUCT", "start": 24, "end": 32},
    {"text": "basil",    "label": "PRODUCT", "start": 46, "end": 51}
  ],
  "gold": [
    {"span_start": 10, "span_end": 17, "gold_uri": "http://aispire.example.org/recipes/Italian"},
    {"span_start": 24, "span_end": 32, "gold_uri": "http://aispire.example.org/recipes/eggplant"},
    {"span_start": 46, "span_end": 51, "gold_uri": "http://aispire.example.org/recipes/basil"}
  ]
}
```

- `text` is the source snippet.
- `ner_spans` is the input your `link()` function receives — the spaCy-style NER output (surface form, label, char offsets).
- `gold` is the supervised target. `gold_uri` is `null` for **NIL** spans (mentions with no candidate in the KG).

## Annotation conventions

- About 18% of surface forms are ambiguous (e.g., `orange` → `:orangeFruit` vs. `:orangeColor`; `turkey` → `:turkeyMeat` vs. `:turkeyCuisine`). The gold label resolves the ambiguity from context.
- About 7% of mentions are NIL — the surface form (e.g., `cinnamon`, `quinoa`, `priya`, `peruvian`) is not in the KG, so `gold_uri` is `null`.
- Char offsets are over the `text` field, half-open `[start, end)`.

## Regenerating

The files are produced deterministically by `_generate.py` (random seed 20260531). Future maintainers can rebuild from the same vocabulary by running:

```bash
cd starter
python -m data._generate
```

Re-running with the same seed produces byte-identical output. `_generate.py` is a developer helper, not part of the learner workflow.
