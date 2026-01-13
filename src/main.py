import json
from pathlib import Path

from src.core.pipeline import run_pipeline

OUTPUT_FILE = Path("outputs/result.json")


def main():
    title = input("Enter journal/article title: ").strip()

    if not title:
        print("Error: Title cannot be empty.")
        return

    result = run_pipeline(title)

    output = {
        "input_title": title,
        **result
    }

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))
    print(f"\nOutput saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()