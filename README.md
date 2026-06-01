# Lab 9B — Entity Linking

Follow the learner-facing lab guide on the AISPIRE course site:
`https://levelup-applied-ai.github.io/aispire-14005-pages/modules/module-9/8c879c64`

**Deliverables:**

1. Implement `linker/lookup.py::candidates()` — SKOS-mediated candidate generation via parameterized SPARQL against the Fuseki endpoint.
2. Implement `linker/disambiguate.py::disambiguate()` — type-compatibility filter (using `NER_LABEL_TO_KG_TYPE`) plus one additional signal (co-occurrence or `rdfs:subClassOf` entailment).
3. Implement `linker/link.py::link()` — orchestrate candidate generation + disambiguation; populate `LinkResult` for each input span.
4. Implement `linker/score.py::score()` — precision / recall / F1 per the methodology in the docstring.
5. Extend `linker/ner_to_kg_type.py::NER_LABEL_TO_KG_TYPE` to cover the NER labels you see in `data/dev.jsonl`.
6. Open a PR from a `lab-9b` branch with a one-paragraph summary of your second disambiguation signal and your dev-split P/R/F1.

Local run:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
docker compose up -d
python load_dataset.py
pytest tests/ -v
```

Convenience: `python run_dev_eval.py` runs your linker against `data/dev.jsonl` and prints P/R/F1 for tuning.

---

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio. Redistribution outside this course is not permitted.
