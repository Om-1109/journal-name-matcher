from typing import Dict
from .normalize import normalize_title

TITLE_COLUMN = "article_title"  # ✅ corrected column name

def exact_and_normalized_match(input_title: str, dataset) -> Dict:
    """
    Performs exact and normalized matching against the dataset.
    """

    # Exact raw match
    raw_matches = dataset[dataset[TITLE_COLUMN] == input_title]

    # Normalized match
    normalized_input = normalize_title(input_title)
    dataset["_normalized"] = dataset[TITLE_COLUMN].apply(normalize_title)

    normalized_matches = dataset[
        dataset["_normalized"] == normalized_input
    ]

    return {
        "exact_match": not raw_matches.empty,
        "normalized_match": not normalized_matches.empty,
        "exact_matches": raw_matches[TITLE_COLUMN].tolist(),
        "normalized_matches": normalized_matches[TITLE_COLUMN].tolist()
    }