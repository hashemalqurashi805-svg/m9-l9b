"""Linker orchestrator.

Wires candidates() -> disambiguate() into one pass over the NER spans of
a document, producing one LinkResult per span.
"""
from linker.candidates import candidates
from linker.disambiguate import disambiguate
from linker.types import LinkResult


def link(
    driver,
    doc_id: str,
    text: str,
    ner_spans: list[tuple[int, int, str, str]],
) -> list[LinkResult]:
    """Orchestrate the linker pipeline for one document."""
    
    # 1. Initialize results = [] and doc_resolved = [].
    results = []
    doc_resolved = []
    
    # 2. For each (start, end, surface, ner_label) in ner_spans (in order):
    for start, end, surface, ner_label in ner_spans:
        
        # a. Call candidates(driver, surface).
        cands = candidates(driver, surface)
        
        # b. Call disambiguate(driver, candidates_list, ner_label, doc_resolved).
        chosen_cand, reason = disambiguate(driver, cands, ner_label, doc_resolved)
        
        # c. Construct a LinkResult (predicted_node_id/predicted_type_label from chosen candidate dict, or None on NIL).
        predicted_node_id = chosen_cand["id"] if chosen_cand else None
        predicted_type_label = chosen_cand["labels"][0] if chosen_cand and chosen_cand["labels"] else None
        
        result = LinkResult(
            doc_id=doc_id,
            start=start,
            end=end,
            surface=surface,
            predicted_node_id=predicted_node_id,
            predicted_type_label=predicted_type_label,
            reason=reason
        )
        
        # d. Append it to results AND to doc_resolved.
        results.append(result)
        doc_resolved.append(result)
        
    # 3. Return results.
    return results