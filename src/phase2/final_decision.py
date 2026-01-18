def make_final_decision(journal_predictions):
    """
    Convert similarity scores into human-readable decision.
    Tuned for research-domain abstracts.
    """

    if not journal_predictions:
        return "Journal is novel"

    top_score = journal_predictions[0].get("score", 0.0)

    if top_score >= 0.6:
        return "Journal likely exists"
    elif top_score >= 0.35:
        return "Journal possibly exists"
    else:
        return "Journal is likely novel"
