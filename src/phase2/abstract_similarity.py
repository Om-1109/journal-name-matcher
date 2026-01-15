import re
from collections import Counter

def extract_semantics(text: str) -> dict:
    text = text.lower()

    keywords = list(set(re.findall(r"\b[a-z]{4,}\b", text)))

    domain = keywords[:5]
    problem = keywords[5:10]
    techniques = keywords[10:15]

    return {
        "domain": set(domain),
        "problem": set(problem),
        "techniques": set(techniques),
        "keywords": set(keywords),
    }


def overlap(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def compute_abstract_similarity(user_abstract: str, existing_abstract: str) -> dict:
    u = extract_semantics(user_abstract)
    e = extract_semantics(existing_abstract)

    return {
        "domain_match": overlap(u["domain"], e["domain"]),
        "problem_overlap": overlap(u["problem"], e["problem"]),
        "technique_overlap": overlap(u["techniques"], e["techniques"]),
        "keyword_overlap": overlap(u["keywords"], e["keywords"]),
    }