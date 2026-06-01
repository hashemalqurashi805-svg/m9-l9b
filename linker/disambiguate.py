"""Pick the single best URI from a candidate set, or return NIL.

Disambiguation runs only when ``candidates()`` returned more than one URI.
Single-candidate and zero-candidate cases are handled in ``link()``.
"""

from typing import Optional


def disambiguate(
    candidate_uris: list[str],
    ner_label: str,
    doc_context: dict,
    endpoint: str,
) -> Optional[str]:
    """Return the single best candidate URI, or ``None`` (NIL).

    Apply two signals, in order:

    1. **Type compatibility** — keep only candidates whose ``rdf:type`` is
       compatible with ``ner_label`` according to ``NER_LABEL_TO_KG_TYPE``.
    2. **One additional signal of your choice** — co-occurrence with other
       already-linked entities in ``doc_context``, OR ``rdfs:subClassOf``
       entailment so a sub-type candidate counts as compatible with a
       parent-typed NER label. Pick one and describe it in the PR.

    Returns the single survivor when exactly one candidate remains after
    both stages, otherwise ``None``. Prefer precision over recall: when
    two or more candidates are tied after both signals, return ``None``.

    ``doc_context`` carries information your second signal needs (e.g., the
    set of URIs already linked elsewhere in the same document, or the
    surrounding text). The exact shape is the learner's design choice.
    """
    # TODO: filter candidate_uris to those whose rdf:type is compatible with
    # ner_label via NER_LABEL_TO_KG_TYPE. If exactly one survives, return it.
    # If zero survive, return None.
    # TODO: if two or more survive, apply your second signal (co-occurrence
    # or subClassOf entailment) and return the single best — or None on ties.
    raise NotImplementedError("Implement disambiguate() — see the lab guide for the task description.")
