import re
from typing import Dict, List

DOMAIN_KEYWORDS = {
    "networking": ["network", "routing", "latency", "bandwidth", "topology"],
    "wireless": ["5g", "wireless", "radio", "cellular"],
    "security": ["security", "attack", "encryption", "privacy"],
    "distributed systems": ["distributed", "fault tolerance", "replication"],
}

TECHNIQUE_KEYWORDS = {
    "graph algorithms": [
        "spanner", "graph", "shortest path",
        "topology", "sparse graph"
    ],
    "network optimization": [
        "latency", "bandwidth", "routing", "performance"
    ],
    "simulation": ["simulation", "simulated"]
}


def extract_dataset_semantics(text: str) -> Dict[str, List[str]]:
    text = text.lower()

    domains = [
        d for d, words in DOMAIN_KEYWORDS.items()
        if any(w in text for w in words)
    ]

    techniques = [
        tech for tech, words in TECHNIQUE_KEYWORDS.items()
        if any(w in text for w in words)
    ]

    seen = []
    for k in re.findall(r"\b[a-z]{6,}\b", text):
        if k not in seen:
            seen.append(k)

    return {
        "domain": domains[0] if domains else "",
        "techniques": techniques,
        "keywords": seen[:10],
    }