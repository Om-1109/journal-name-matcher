import pandas as pd
from src.detection.semantic_match import SemanticMatcher

def test_semantic_similarity():
    data = pd.DataFrame({
        "article_title": [
            "Journal based on computer networks",
            "Advanced Artificial Intelligence"
        ]
    })

    matcher = SemanticMatcher(threshold=0.70)

    results = matcher.find_similar(
        "Journal about computer networks",
        data
    )

    assert len(results) > 0
    assert results[0]["similarity_score"] >= 0.70