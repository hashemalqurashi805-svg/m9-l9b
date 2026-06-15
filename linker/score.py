"""Linker P/R/F1 scoring."""
from linker.types import LinkResult, GoldSpan

def score(predictions: list[LinkResult], gold: list[GoldSpan]) -> dict:
    gold_map = {(g.doc_id, g.start, g.end): g for g in gold}
    preds_map = {(p.doc_id, p.start, p.end): p for p in predictions}
    
    doc_metrics = {}
    all_doc_ids = {g.doc_id for g in gold}
    
    for doc_id in all_doc_ids:
        tp, fp, fn = 0, 0, 0
        all_spans = {s for s in gold_map if s[0] == doc_id} | {s for s in preds_map if s[0] == doc_id}
        
        for span in all_spans:
            g = gold_map.get(span)
            p = preds_map.get(span)
            
            is_gold_nil = (g is None or g.gold_node_id is None)
            is_pred_nil = (p is None or p.predicted_node_id is None)
            
            if not is_gold_nil and not is_pred_nil:
                if p.predicted_node_id == g.gold_node_id and p.predicted_type_label == g.gold_type_label:
                    tp += 1
                else:
                    fp += 1
                    fn += 1
            elif not is_gold_nil and is_pred_nil:
                fn += 1
            elif is_gold_nil and not is_pred_nil:
                fp += 1
                
        doc_metrics[doc_id] = (tp, fp, fn)

    total_p, total_r, total_f1 = 0.0, 0.0, 0.0
    count = len(doc_metrics)
    
    for tp, fp, fn in doc_metrics.values():
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        total_p += precision
        total_r += recall
        total_f1 += f1
        
    return {
        "precision": total_p / count if count else 0.0,
        "recall": total_r / count if count else 0.0,
        "f1": total_f1 / count if count else 0.0
    }