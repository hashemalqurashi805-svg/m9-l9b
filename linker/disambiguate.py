"""Disambiguate candidates against the recipe KG."""

NER_LABEL_TO_KG_TYPE: dict[str, set[str]] = {
    "PERSON": {"Author"},
    "ORG": {"Author"},
    "GPE": {"Cuisine"},
    "FOOD": {"Ingredient", "Cuisine"},
    "INGREDIENT": {"Ingredient"},
    "TECHNIQUE": {"Technique"},
    "RECIPE": {"Recipe"}
}

def disambiguate(driver, candidates_: list[dict], ner_label: str, doc_resolved: list) -> tuple[dict | None, str]:
    if not candidates_:
        return None, "nil-no-candidates"
    if len(candidates_) == 1:
        return candidates_[0], "resolved-unique"

    allowed_types = NER_LABEL_TO_KG_TYPE.get(ner_label, set())

    # 1. توافق النوع
    type_matches = [c for c in candidates_ if any(l in allowed_types for l in c["labels"])]
    if len(type_matches) == 1:
        return type_matches[0], "resolved-by-type"

    # 2. التوافق الهرمي
    hierarchical_matches = []
    with driver.session() as session:
        for c in candidates_:
            query = "MATCH (c:Entity {id: $cand_id})-[:SUBCLASS_OF*0..]->(ancestor:Entity) RETURN collect(labels(ancestor)) AS ancestor_labels"
            result = session.run(query, cand_id=c["id"]).single()
            if result:
                all_ancestor_labels = {label for sublist in result["ancestor_labels"] for label in sublist}
                if any(t in all_ancestor_labels for t in allowed_types):
                    hierarchical_matches.append(c)
    if len(hierarchical_matches) == 1:
        return hierarchical_matches[0], "resolved-by-hierarchy"

    # 3. تكرار القفزة الواحدة (مع حماية المتغير)
    resolved_ids = [res.predicted_node_id for res in doc_resolved if res.predicted_node_id] if doc_resolved else []
    
    if resolved_ids:
        best_cand, max_overlap = None, 0
        with driver.session() as session:
            for c in candidates_:
                query = "MATCH (c:Entity {id: $cand_id})-[]-(neighbor:Entity) WHERE neighbor.id IN $resolved_ids RETURN count(neighbor) AS overlap"
                result = session.run(query, cand_id=c["id"], resolved_ids=resolved_ids).single()
                overlap = result["overlap"] if result else 0
                if overlap > max_overlap:
                    max_overlap, best_cand = overlap, c
        if best_cand and max_overlap > 0:
            return best_cand, "resolved-by-context"

    return None, "nil-ambiguous"