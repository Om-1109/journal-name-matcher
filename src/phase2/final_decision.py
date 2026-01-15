from typing import List, Dict, Any


def make_final_decision(journals):
    if not journals:
        return "Novel journal"

    max_similarity = journals[0]["avg_similarity"]

    if max_similarity >= 0.75:
        verdict = "Journal already exists"
    elif max_similarity >= 0.45:
        verdict = "Journal is redundant"
    else:
        verdict = "Journal is novel"

    return verdict