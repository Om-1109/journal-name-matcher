def jaccard_similarity(a, b):
    if not a or not b:
        return 0.0
    return len(set(a) & set(b)) / len(set(a) | set(b))


def compute_structured_similarity(user, dataset) -> float:
    score = 0.0

    # Domain match
    if user["domain"] == dataset["domain"]:
        score += 0.4

    # Techniques overlap
    common_tech = set(user["techniques"]) & set(dataset["techniques"])
    score += 0.3 * (len(common_tech) / max(len(user["techniques"]), 1))

    # Keywords overlap
    common_keys = set(user["keywords"]) & set(dataset["keywords"])
    score += 0.3 * (len(common_keys) / max(len(user["keywords"]), 1))

    return round(min(score, 1.0), 3)