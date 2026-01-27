import json
from typing import Dict, List
from src.phase2.llm_client import call_llm

# -----------------------------------
# Cache configuration
# -----------------------------------
CACHE_PATH = Path("data/abstract_semantics_cache.json")


def load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {}

    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        # Corrupted or invalid cache → reset safely
        return {}


def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def extract_semantics_from_abstract(abstract: str) -> dict:
    """
    Extract semantic structure from abstract using LLM.
    Always returns a dictionary.
    Never crashes on bad output.
    """

    cache = load_cache()

    # Stable lightweight cache key
    key = abstract.strip()[:200]

    if key in cache:
        return cache[key]

    prompt = f"""
Extract structured information from the abstract.

Return STRICT JSON only.

Fields:
- domain (string)
- techniques (list of strings)
- keywords (list of strings)

Abstract:
{abstract}
"""

    # -------------------------------
    # Call LLM safely
    # -------------------------------
    raw = call_llm(prompt)

    if not raw or not raw.strip():
        result = {}
    else:
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            # LLM returned invalid JSON
            result = {}

    # Cache even empty result to avoid repeated calls
    cache[key] = result
    save_cache(cache)

    return result
