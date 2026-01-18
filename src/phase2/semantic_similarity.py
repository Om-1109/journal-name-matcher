def normalize_list(items):
    """
    Convert list items into hashable lowercase strings.
    Handles strings, dicts, None, and mixed types safely.
    """
    normalized = []

    for item in items or []:
        if isinstance(item, str):
            normalized.append(item.lower())
        elif isinstance(item, dict):
            for v in item.values():
                if isinstance(v, str):
                    normalized.append(v.lower())
                    break
        elif item is not None:
            normalized.append(str(item).lower())

    return normalized


def normalize_domain(value):
    """
    Normalize domain field to lowercase string.
    """
    if isinstance(value, str):
        return value.lower()
    return ""


def jaccard_similarity(a, b):
    a_norm = normalize_list(a)
    b_norm = normalize_list(b)

    if not a_norm or not b_norm:
        return 0.0

    a_set, b_set = set(a_norm), set(b_norm)
    return len(a_set & b_set) / len(a_set | b_set)


def compute_structured_similarity(user: dict, dataset: dict) -> float:
    """
    Compute similarity between structured semantic representations.
    Fully robust against malformed LLM output.
    """

    score = 0.0

    # -------------------------------
    # Domain match
    # -------------------------------
    user_domain = normalize_domain(user.get("domain"))
    dataset_domain = normalize_domain(dataset.get("domain"))

    if user_domain and dataset_domain and user_domain == dataset_domain:
        score += 0.4

    # -------------------------------
    # Techniques overlap
    # -------------------------------
    tech_sim = jaccard_similarity(
        user.get("techniques", []),
        dataset.get("techniques", [])
    )
    score += 0.3 * tech_sim

    # -------------------------------
    # Keywords overlap
    # -------------------------------
    key_sim = jaccard_similarity(
        user.get("keywords", []),
        dataset.get("keywords", [])
    )
    score += 0.3 * key_sim

    return round(min(score, 1.0), 3)
