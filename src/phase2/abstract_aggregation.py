from collections import defaultdict


def aggregate_abstract_results(article_results):
    journal_map = defaultdict(list)

    for r in article_results:
        journal_map[r["journal_name"]].append(r["similarity"])

    aggregated = []

    for journal, scores in journal_map.items():
        aggregated.append({
            "journal_name": journal,
            "avg_similarity": round(sum(scores) / len(scores), 3),
            "max_similarity": round(max(scores), 3),
            "article_matches": len(scores),
        })

    return sorted(
        aggregated,
        key=lambda x: x["avg_similarity"],
        reverse=True
    )