from collections import defaultdict


def aggregate_abstract_results(results):
    journal_scores = {}

    for r in results:
        j = r["journal_name"]
        score = r["similarity"]

        if j not in journal_scores:
            journal_scores[j] = score
        else:
            journal_scores[j] = max(journal_scores[j], score)

    aggregated = [
        {
            "journal_name": j,
            "max_similarity": round(score, 3)
        }
        for j, score in journal_scores.items()
    ]

    return sorted(aggregated, key=lambda x: x["max_similarity"], reverse=True)