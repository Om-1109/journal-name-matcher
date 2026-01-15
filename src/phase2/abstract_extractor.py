import json
from pathlib import Path
from src.phase2.llm_client import call_llm

CACHE_PATH = Path("data/abstract_semantics_cache.json")

def load_cache():
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text())
    return {}

def save_cache(cache):
    CACHE_PATH.write_text(json.dumps(cache, indent=2))

def extract_semantics_from_abstract(abstract: str) -> dict:
    cache = load_cache()

    key = abstract.strip()[:200]  # stable lightweight key

    if key in cache:
        return cache[key]

    prompt = f"""
Extract the following information from the research abstract.

Return STRICT JSON only.

Fields:
- domain
- techniques (list)
- keywords (list)

Abstract:
{abstract}
"""

    raw = call_llm(prompt)
    result = json.loads(raw)

    cache[key] = result
    save_cache(cache)

    return result