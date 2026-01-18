import pandas as pd
from pathlib import Path

from src.core.pipeline import run_pipeline
from src.phase2.abstract_pipeline import run_phase2


# -------------------------------
# Resolve project root safely
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "master_journals.csv"


def read_multiline_input():
    print("(Paste abstract. Type END on a new line to finish)\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    while True:
        title = input("Enter journal/article title: ").strip()

        if not title:
            print("Error: Title cannot be empty.")
            continue

        # Phase 1
        phase1 = run_pipeline(title)
        journal_predictions = phase1.get("journal_predictions", [])

        if (
            journal_predictions
            and journal_predictions[0]
            .get("confidence", "")
            .startswith("Strong")
        ):
            print("\nA journal with a very similar scope already exists.")
            print("Please enter a NEW article title.\n")
            continue

        # Phase 2
        print("\nPhase 2 required. Please enter article abstract:\n")
        user_abstract = read_multiline_input()

        if not user_abstract.strip():
            print("Error: Abstract cannot be empty.")
            continue

        phase2 = run_phase2(
            user_abstract=user_abstract,
            candidate_journals=journal_predictions,
            df=df,
        )

        print("\nFINAL DECISION:")
        print(phase2.get("final_decision", "No decision returned"))
        break


if __name__ == "__main__":
    main()
