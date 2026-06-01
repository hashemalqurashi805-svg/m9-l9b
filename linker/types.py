"""Shared dataclasses for the entity linker.

Fully implemented — learners may import but should not modify.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LinkResult:
    """One linker output for a single NER span.

    Attributes
    ----------
    span : str
        The surface form of the NER span (the text the linker saw).
    predicted_uri : Optional[str]
        The URI the linker resolved the span to, or ``None`` for NIL.
    reason : str
        One of:
        ``"resolved-unique"`` — a single candidate matched (no disambiguation needed)
        ``"resolved-by-type"`` — disambiguation picked a candidate via type compatibility
        ``"resolved-by-context"`` — disambiguation picked a candidate via the
        learner's second signal (co-occurrence or subClassOf entailment)
        ``"nil-no-candidates"`` — no candidate matched the surface form
        ``"nil-ambiguous"`` — multiple candidates survived all disambiguation signals
    start : int
        Character offset of the span start in the source text.
    end : int
        Character offset of the span end (exclusive).
    """

    span: str
    predicted_uri: Optional[str]
    reason: str
    start: int
    end: int
