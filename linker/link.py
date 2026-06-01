"""Orchestrate candidate generation and disambiguation over a set of NER spans."""

from linker.lookup import DEFAULT_ENDPOINT
from linker.types import LinkResult


def link(text: str, ner_spans: list[dict], endpoint: str = DEFAULT_ENDPOINT) -> list[LinkResult]:
    """Link each NER span in ``text`` to a KG URI (or NIL).

    Each item in ``ner_spans`` is a dict with keys ``text`` (surface form),
    ``label`` (NER label string), ``start`` (char offset), ``end`` (exclusive
    char offset).

    For every input span, produce one ``LinkResult`` in the returned list,
    in the same order. ``reason`` must always be populated — even on NIL
    outcomes — so downstream debugging can attribute failures.

    Returns a list of ``LinkResult`` of the same length as ``ner_spans``.
    """
    # TODO: for each span, call candidates(); branch on the size of the
    # returned set:
    #   - zero candidates -> NIL with reason "nil-no-candidates"
    #   - one candidate   -> resolved with reason "resolved-unique"
    #   - multiple        -> call disambiguate(); resolved-by-type / -by-context
    #                        on success, "nil-ambiguous" on failure
    # TODO: assemble doc_context for disambiguate() — e.g., the set of
    # already-resolved URIs on previously-processed spans in the same doc.
    raise NotImplementedError("Implement link() — see the lab guide for the task description.")
