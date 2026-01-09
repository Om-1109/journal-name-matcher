import argparse
import json
from pathlib import Path

from src.core.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Journal Name Matcher CLI"
    )
    parser.add_argument(
        "title",
        type=str,
        help="Journal title to detect"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/detection.yaml"),
        help="Path to detection config YAML"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    result = run_pipeline(
        input_title=args.title,
        config_path=args.config,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
