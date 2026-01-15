import sys
import pandas as pd

from src.core.pipeline import run_pipeline
from src.phase2.abstract_pipeline import run_phase2


DATA_PATH = "/Users/dhruvgourisaria/JournalProject/journal-name-matcher/journal-name-matcher/data/master_journals.csv"


def read_multiline_input():
    print("(Paste abstract. Press Ctrl+D to finish)\n")
    return sys.stdin.read().strip()


def main():
    df = pd.read_csv(DATA_PATH)

    while True:
        title = input("Enter journal/article title: ").strip()

        if not title:
            print("Error: Title cannot be empty.")
            continue

        phase1 = run_pipeline(title)
        journal_predictions = phase1["journal_predictions"]

        # Strong match → stop
        if journal_predictions and journal_predictions[0]["confidence"].startswith("Strong"):
            print("\nA journal with a very similar scope already exists.")
            print("Please enter a NEW article title.\n")
            continue

        # Phase 2 required
        print("\nPhase 2 required. Please enter article abstract:\n")
        user_abstract = read_multiline_input()

        if not user_abstract:
            print("Error: Abstract cannot be empty.")
            continue

        phase2 = run_phase2(
            user_abstract=user_abstract,
            candidate_journals=journal_predictions,
            df=df,
        )

        print("\nFINAL DECISION:")
        print(phase2["final_decision"])
        break


if __name__ == "__main__":
    main()