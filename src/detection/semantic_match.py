from sentence_transformers import SentenceTransformer
from .similarity_utils import cosine_similarity

TITLE_COLUMN = "article_title"  # ✅ corrected column name

class SemanticMatcher:
    """
    Semantic matcher using sentence embeddings + cosine similarity.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2", threshold=0.80):
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold

    def find_similar(self, input_title: str, dataset):
        """
        Returns semantically similar article titles with similarity scores.
        """
        input_embedding = self.model.encode(input_title)

        results = []

        for title in dataset[TITLE_COLUMN]:
            title_embedding = self.model.encode(title)
            score = cosine_similarity(input_embedding, title_embedding)

            if score >= self.threshold:
                results.append({
                    "article_title": title,
                    "similarity_score": round(score, 3)
                })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results