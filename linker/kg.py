"""KG plumbing — connect an rdflib ``Graph`` to the live Fuseki endpoint.

Fully implemented helper. Learners may use ``connect()`` to obtain a graph
they can run parameterized SPARQL against (via ``Graph.query(q,
initBindings=...)``) without each module re-implementing the HTTP wiring.

This is plumbing, not the lab's pedagogy — the lab is about candidate
generation, disambiguation, NIL handling, and P/R/F1; the lab is not about
how to wire an rdflib store to a SPARQL endpoint.
"""

from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore

DEFAULT_ENDPOINT = "http://localhost:3030/recipes/sparql"


def connect(endpoint: str = DEFAULT_ENDPOINT) -> Graph:
    """Return an rdflib ``Graph`` backed by the Fuseki endpoint at ``endpoint``.

    The returned graph is read-only from the learner's perspective —
    Fuseki was populated by ``load_dataset.py`` after ``docker compose up``.
    Use ``Graph.query(q, initBindings={...})`` for parameterized queries.
    """
    return Graph(SPARQLStore(query_endpoint=endpoint))
