import pandas as pd
from typing import List

from src.phase2.abstract_extractor import extract_semantics_from_abstract
from src.phase2.semantic_similarity import compute_structured_similarity
from src.phase2.abstract_aggregation import aggregate_abstract_results
from src.phase2.final_decision import make_final_decision

MAX_DATASET_ROWS = 1352

# HARD SAFETY LIMIT (CRITICAL)
MAX_PHASE2_ARTICLES = 5


def _empty_semantics() -> Dict:
    """Default safe semantics structure."""
    return {
        "domain": "",
        "techniques": [],
        "keywords": [],
    }


def get_cached_semantics(abstract: str) -> Dict:
    """
    Extracts structured semantics with caching.
    Always returns a safe dictionary.
    """
    abstract = abstract.strip()
    if not abstract:
        return _empty_semantics()

    if abstract not in SEMANTIC_CACHE:
        semantics = extract_semantics_from_abstract(abstract)

        if not isinstance(semantics, dict):
            semantics = _empty_semantics()
        else:
            semantics.setdefault("domain", "")
            semantics.setdefault("techniques", [])
            semantics.setdefault("keywords", [])

        SEMANTIC_CACHE[abstract] = semantics

    return SEMANTIC_CACHE[abstract]


def run_phase2(
    user_abstract: str,
    candidate_journals: List[dict],
    df: pd.DataFrame
) -> dict:
    """
    Phase 2 pipeline using structured abstract comparison.
    GUARANTEED to terminate.
    """

    # -----------------------------
    # USER SEMANTICS
    # -----------------------------
    print("\n[Phase 2] Extracting semantics from user abstract (LLM call)…")
    user_semantics = get_cached_semantics(user_abstract)

    allowed = {j["journal_name"] for j in candidate_journals}
    article_results = []

    # Only evaluate journals shortlisted in Phase 1
    allowed_journals = {
        j.get("journal_name", "").strip()
        for j in candidate_journals
    }

    if not allowed_journals:
        return {
            "user_semantics": user_semantics,
            "journal_predictions": [],
            "final_decision": "NO CANDIDATE JOURNALS AFTER PHASE 1",
        }

    print(
        f"[Phase 2] Comparing against {len(allowed_journals)} candidate journals "
        f"(max {MAX_PHASE2_ARTICLES} abstracts)…"
    )

    # -----------------------------
    # DATASET LOOP (LIMITED)
    # -----------------------------
    processed = 0

    for _, row in df.iterrows():

        if processed >= MAX_PHASE2_ARTICLES:
            break

        journal_name = str(row.get("journal_name", "")).strip()
        abstract = str(row.get("abstract", "")).strip()

        if not journal_name or journal_name not in allowed_journals:
            continue

        dataset_semantics = {
            "domain": str(row.get("domain", "")).lower().strip(),
            "techniques": _norm(row.get("techniques")),
            "keywords": _norm(row.get("keywords")),
        }

        print(f"[Phase 2] Processing abstract {processed + 1}/{MAX_PHASE2_ARTICLES}")

        dataset_semantics = get_cached_semantics(abstract)

        similarity = compute_structured_similarity(
            user_semantics,
            dataset_semantics
        )

        article_results.append({
            "journal_name": journal,
            "similarity": similarity
        })

        processed += 1

    if not article_results:
        return {
            "user_semantics": user_semantics,
            "journal_predictions": [],
            "final_decision": "NO MATCHING ABSTRACTS FOUND FOR PHASE 2",
        }

    # -----------------------------
    # AGGREGATION + DECISION
    # -----------------------------
    journal_predictions = aggregate_abstract_results(article_results)

    return {
        "user_semantics": user_semantics,
        "journal_predictions": journal_predictions,
        "final_decision": final_decision,
    }
