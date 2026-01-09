from typing import Dict, List, Any

# ============================
# Safe imports from detection
# ============================

try:
    from src.detection.exact import exact_match_titles
except Exception:
    exact_match_titles = None

try:
    from src.detection.semantic import semantic_match_titles
except Exception:
    semantic_match_titles = None


# ============================
# Public Integration Function
# ============================

def detect_journal(input_title: str) -> Dict[str, Any]:
    """
    Integration-layer journal detection.

    This function:
    - Does NOT implement detection logic
    - Does NOT normalize input
    - ONLY calls detection functions owned by Person A
    - Returns a stable, contract-safe response

    Args:
        input_title (str): Raw journal title provided by user

    Returns:
        dict: Detection results following FINAL CONTRACT
    """

    exact_matches: List[str] = []
    semantic_matches: List[Dict[str, Any]] = []

    # ----------------------------
    # Exact Matching
    # ----------------------------
    if callable(exact_match_titles):
        try:
            exact_matches = exact_match_titles(input_title) or []
        except Exception:
            exact_matches = []

    # ----------------------------
    # Semantic / Fuzzy Matching
    # ----------------------------
    if callable(semantic_match_titles):
        try:
            semantic_matches = semantic_match_titles(input_title) or []
        except Exception:
            semantic_matches = []

    # ----------------------------
    # Derived Flags
    # ----------------------------
    exact_match_found = len(exact_matches) > 0
    normalized_match_found = exact_match_found or len(semantic_matches) > 0

    # ----------------------------
    # Final Contract
    # ----------------------------
    return {
        "exact_match": exact_match_found,
        "normalized_match": normalized_match_found,
        "exact_matches": exact_matches,
        "semantic_matches": semantic_matches,
    }
