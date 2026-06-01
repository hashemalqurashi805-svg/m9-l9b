"""Candidate generation against the live Fuseki endpoint.

The function talks to Fuseki via an rdflib ``Graph`` backed by ``SPARQLStore``
— the same ``Graph.query(q, initBindings=...)`` API the M9 Week B drill
used against an in-memory graph, now pointed at a remote endpoint. The KG
was POSTed into the ``recipes`` dataset by ``load_dataset.py``.

The SPARQL query body itself must not contain the surface form as text;
the surface form is passed as a parameter binding.
"""

from linker.kg import DEFAULT_ENDPOINT, connect  # noqa: F401  (DEFAULT_ENDPOINT re-exported)


def candidates(surface_form: str, endpoint: str = DEFAULT_ENDPOINT) -> list[str]:
    """Return KG URIs whose SKOS label matches ``surface_form``.

    A match is any entity carrying a ``skos:prefLabel`` or ``skos:altLabel``
    whose lexical form equals ``surface_form`` case-insensitively.

    Must use a parameterized SPARQL query (no string interpolation of
    ``surface_form`` into the query text).

    Returns the matching URIs as a list of strings; the order is not
    significant — callers compare as a set.
    """
    # TODO: connect to the KG via linker.kg.connect(endpoint) to get an
    # rdflib Graph backed by Fuseki.
    # TODO: write a SPARQL SELECT that matches URIs whose skos:prefLabel
    # OR skos:altLabel equals a parameter variable. The surface form
    # must enter the query as a parameter — not as interpolated text in
    # the query body. Use the same parameterized rdflib query pattern as
    # the drill (Graph.query(q, initBindings=...)); think about which
    # variable to bind and how to make the match case-insensitive given
    # how labels are stored in the KG.
    # TODO: execute the query and collect the resulting URI strings.
    raise NotImplementedError("Implement candidates() — see the lab guide for the task description.")
