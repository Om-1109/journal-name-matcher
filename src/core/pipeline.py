from pathlib import Path
from typing import Any, Dict

import pandas as pd

from src.core.config import load_config
from src.core.detector import detect_journal

# ============================
# Optional detection init hook
# ============================

try:
    from src.detection.bootstrap import initialize_detection
except Exception:
    initialize_detection = None


# ============================
# Constants
# ============================

DEFAULT_CONFIG_PATH = Path("configs/detection.yaml")
DATASET_PATH = Path("data/master_journals.csv")


# ============================
# Pipeline
# ============================

def run_pipeline(
    input_title: str,
    config_path: Path = DEFAULT_CONFIG_PATH,
) -> Dict[str, Any]:
    """
    End-to-end journal detection pipeline.

    This pipeline:
    - Loads validated configuration
    - Loads dataset in READ-ONLY mode
    - Initializes detection components (if supported)
    - Calls detect_journal()

    Args:
        input_title (str): Raw journal title
        config_path (Path): Path to detection config YAML

    Returns:
        dict: detect_journal() response
    """

    # ----------------------------
    # Load configuration
    # ----------------------------
    config = load_config(config_path)

    # ----------------------------
    # Load dataset (READ-ONLY)
    # ----------------------------
    if not DATASET_PATH.exists():
        raise RuntimeError(f"Dataset not found: {DATASET_PATH}")

    dataset_df = pd.read_csv(DATASET_PATH)

    # ----------------------------
    # Initialize detection layer
    # ----------------------------
    # This is OPTIONAL and depends on Person A
    if callable(initialize_detection):
        try:
            initialize_detection(
                dataset=dataset_df,
                config=config.detection,
            )
        except Exception as e:
            raise RuntimeError(
                f"Detection initialization failed: {e}"
            ) from e

    # ----------------------------
    # Run detection
    # ----------------------------
    return detect_journal(input_title)
