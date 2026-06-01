"""Precision / recall / F1 against a gold set."""


def score(predictions: list[dict], gold: list[dict]) -> dict:
    """Compute macro-averaged precision / recall / F1 for the linker.

    Each item in ``predictions`` is a dict with keys ``doc_id``, ``start``,
    ``end``, ``predicted_uri`` (``None`` for NIL). Each item in ``gold`` has
    the same keys with ``gold_uri`` instead of ``predicted_uri`` (``None``
    for NIL).

    Evaluation Methodology (identical to the lab spec and the learner lab guide
    — this is the THIRD statement under the Evaluation Methodology Rule):

    - **Filter** ``predictions`` to the ``(doc_id, start, end)`` keys present
      in ``gold`` before scoring. A prediction whose key is not in gold is
      dropped (not counted as a false positive).
    - **Counting rules** for each gold key:

      * **True positive** iff the predicted URI exactly matches the gold URI
        AND the gold URI is not NIL.
      * **False positive** iff the prediction is a non-NIL URI different
        from the gold URI (mismatch, including the case where gold is NIL
        and the prediction is some URI).
      * **False negative** iff the gold URI is non-NIL but the prediction is
        NIL or missing.
      * **True negative** iff both the gold URI and the prediction are NIL
        — **excluded from precision and recall denominators**.
    - **Macro-average across docs** — compute precision / recall / F1
      per ``doc_id`` first, then average across docs (a doc with no gold
      spans is excluded from the macro average).

    Returns a dict with keys ``precision``, ``recall``, ``f1`` (floats,
    rounded to 4 decimals).
    """
    # TODO: group predictions and gold by doc_id, then by (start, end).
    # TODO: walk each doc, count TP / FP / FN per the rules above, compute
    # per-doc precision/recall/F1, then macro-average across docs.
    raise NotImplementedError("Implement score() — see the lab guide for the task description.")
