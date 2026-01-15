import pandas as pd
from typing import Dict, List

from src.phase2.abstract_extractor import extract_semantics_from_abstract
from src.phase2.semantic_similarity import compute_structured_similarity
from src.phase2.abstract_aggregation import aggregate_abstract_results
from src.phase2.final_decision import make_final_decision


# -----------------------------
# GLOBAL CACHE (IMPORTANT)
# -----------------------------
SEMANTIC_CACHE: Dict[str, Dict] = {}


def get_cached_semantics(abstract: str) -> Dict:
    """
    Extracts structured semantics with caching to avoid repeated LLM calls.
    """
    abstract = abstract.strip()
    if not abstract:
        return {"domain": "", "techniques": [], "keywords": []}

    if abstract not in SEMANTIC_CACHE:
        SEMANTIC_CACHE[abstract] = extract_semantics_from_abstract(abstract)

    return SEMANTIC_CACHE[abstract]


def run_phase2(
    user_abstract: str,
    candidate_journals: List[dict],
    df: pd.DataFrame
) -> dict:
    """
    Phase 2 pipeline using structured abstract comparison.
    """

    # -----------------------------
    # USER SEMANTICS
    # -----------------------------
    user_semantics = get_cached_semantics(user_abstract)

    article_results = []

    # Only evaluate journals shortlisted in Phase 1
    allowed_journals = {j["journal_name"] for j in candidate_journals}

    # -----------------------------
    # DATASET LOOP
    # -----------------------------
    for _, row in df.iterrows():

        journal_name = row.get("journal_name", "").strip()
        abstract = str(row.get("abstract", "")).strip()

        if not journal_name or journal_name not in allowed_journals:
            continue

        if not abstract:
            continue

        dataset_semantics = get_cached_semantics(abstract)

        similarity = compute_structured_similarity(
            user_semantics,
            dataset_semantics
        )

        article_results.append({
            "journal_name": journal_name,
            "similarity": similarity,
        })

    # -----------------------------
    # AGGREGATION + DECISION
    # -----------------------------
    journal_predictions = aggregate_abstract_results(article_results)
    final_decision = make_final_decision(journal_predictions)

    return {
        "user_semantics": user_semantics,
        "journal_predictions": journal_predictions,
        "final_decision": final_decision,
    }