def parse_case_query(query: str):

    q = query.lower()

    crime = None
    situation = None
    confidence = "low"
    explanation = "Could not confidently identify the case."

    # crime matching
    if any(word in q for word in ["steal", "stolen", "snatching", "snatched", "theft", "robbed", "phone stolen", "bike stolen"]):
        crime = "theft"

    elif any(word in q for word in ["online fraud", "cyber fraud", "phishing", "otp scam", "digital scam", "online scam"]):
        crime = "cyber_fraud"

    elif any(word in q for word in ["cheat", "cheating", "money scam", "fraud", "duped", "financial scam"]):
        crime = "cheating_fraud"

    elif any(word in q for word in ["beat", "beating", "fight", "hit", "assault", "attacked"]):
        crime = "assault"

    elif any(word in q for word in ["drug", "drugs", "narcotic", "ganja", "substance"]):
        crime = "drug_possession"


    # situation matching
    if ("night" in q and any(word in q for word in ["picked", "arrested", "taken", "custody"])):
        situation = "arrested_at_night"

    elif any(word in q for word in [
        "questioning",
        "called to station",
        "called for questioning",
        "come to station",
        "asked to come",
        "police called"
    ]):
        situation = "called_for_questioning"

    elif any(word in q for word in [
        "from home",
        "took him from home",
        "picked him from home",
        "taken from home",
        "police came home"
    ]):
        situation = "police_took_from_home"

    elif any(word in q for word in [
        "fir",
        "case registered",
        "complaint registered",
        "fir filed",
        "police complaint"
    ]):
        situation = "fir_registered"


    if crime and situation:
        confidence = "high"
        explanation = f"This looks like a {crime} case with situation '{situation}'."

    elif crime or situation:
        confidence = "medium"
        explanation = "Part of the case could be identified, but not everything clearly."

    return {
        "crime": crime,
        "situation": situation,
        "confidence": confidence,
        "explanation": explanation
    }