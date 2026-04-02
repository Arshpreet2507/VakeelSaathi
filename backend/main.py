from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from db import laws_collection, rights_collection, checklists_collection
from ai_utils import parse_case_query
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Pydantic Models
# -----------------------------
class CaseInput(BaseModel):
    crime: str
    situation: str


class ExplainInput(BaseModel):
    law: dict
    checklist: Optional[dict] = None
    language: str = "en"


class QueryInput(BaseModel):
    query: str


class ChatbotInput(BaseModel):
    query: str
    crime: str
    situation: Optional[str] = None


# -----------------------------
# Basic Health Route
# -----------------------------
@app.get("/api/health")
def home():
    return {"message": "Vakeel Saathi backend is running"}


# -----------------------------
# Parse Free-Text Situation
# -----------------------------
@app.post("/parse-case-query")
def parse_case(data: QueryInput):
    return parse_case_query(data.query)


# -----------------------------
# Structured Guidance Route
# -----------------------------
@app.post("/get-guidance")
def get_guidance(data: CaseInput):
    crime_key = data.crime.lower().replace(" ", "_")
    situation_key = data.situation.lower().replace(" ", "_")

    law = laws_collection.find_one({"offence_key": crime_key}, {"_id": 0})
    checklist = checklists_collection.find_one({"situation_key": situation_key}, {"_id": 0})
    rights = list(rights_collection.find({}, {"_id": 0}))

    if not law:
        return {"message": "No legal guidance found for this crime"}

    return {
        "law": law,
        "checklist": checklist,
        "rights": rights
    }


# -----------------------------
# AI + MongoDB Combined Guidance
# -----------------------------
@app.post("/ai-case-guidance")
def ai_case_guidance(data: QueryInput):
    parsed = parse_case_query(data.query)

    crime = parsed.get("crime")
    situation = parsed.get("situation")

    if not crime:
        return {
            "message": "Could not identify the legal issue clearly.",
            "parsed": parsed
        }

    law = laws_collection.find_one({"offence_key": crime}, {"_id": 0})

    checklist = None
    if situation:
        checklist = checklists_collection.find_one(
            {"situation_key": situation},
            {"_id": 0}
        )

    rights = list(rights_collection.find({}, {"_id": 0}))

    return {
        "parsed_case": parsed,
        "law": law,
        "checklist": checklist,
        "rights": rights
    }


# -----------------------------
# Explain Case in Plain Language
# -----------------------------
@app.post("/explain-case")
def explain_case(data: ExplainInput):
    law = data.law
    checklist = data.checklist
    lang = data.language

    if lang == "hi":
        explanation = _build_hindi_explanation(law, checklist)
    else:
        explanation = _build_english_explanation(law, checklist)

    return {"explanation": explanation}


def _build_english_explanation(law: dict, checklist: Optional[dict]) -> str:
    name = law.get("offence_name", "this offence")
    section = law.get("section", "relevant section")
    explanation = law.get("plain_explanation", "")
    bailable = law.get("bailable", "unknown")
    cognizable = law.get("cognizable", False)
    max_pun = law.get("max_punishment", "as per law")

    bail_text = (
        "This is a <strong>bailable offence</strong>, meaning the accused has a right to get bail."
        if bailable
        else "This is a <strong>non-bailable offence</strong>, meaning bail is not a right and must be granted by a court."
    )

    cog_text = (
        "It is <strong>cognizable</strong>, so police can arrest without a warrant and start investigating immediately."
        if cognizable
        else "It is <strong>non-cognizable</strong>, so police need a magistrate's order to investigate."
    )

    parts = [
        f"<strong>{name}</strong> falls under <strong>{section}</strong> of Indian law.",
        explanation,
        bail_text,
        cog_text,
        f"The maximum punishment is <strong>{max_pun}</strong>.",
    ]

    if checklist:
        title = checklist.get("title", "your situation")
        steps = checklist.get("immediate_steps", [])
        if steps:
            steps_str = ", ".join(steps[:3])
            parts.append(
                f"Since the situation is '<strong>{title}</strong>', you should immediately: {steps_str}."
            )

    next_steps = law.get("next_2_hours", [])
    if next_steps:
        parts.append(
            f"In the next 2 hours, the most important step is: <strong>{next_steps[0]}</strong>."
        )

    parts.append(
        "Remember: every arrested person must be produced before a magistrate within 24 hours and has the right to a lawyer."
    )

    return "<br><br>".join(parts)


def _build_hindi_explanation(law: dict, checklist: Optional[dict]) -> str:
    name = law.get("offence_name", "यह अपराध")
    section = law.get("section", "संबंधित धारा")
    explanation = law.get("plain_explanation", "")
    bailable = law.get("bailable", "unknown")
    cognizable = law.get("cognizable", False)
    max_pun = law.get("max_punishment", "कानून अनुसार")

    bail_text = (
        "यह एक <strong>जमानती अपराध</strong> है, यानी आरोपी को जमानत पाने का अधिकार है।"
        if bailable
        else "यह एक <strong>गैर-जमानती अपराध</strong> है, यानी जमानत अधिकार नहीं है और अदालत से लेनी होगी।"
    )

    cog_text = (
        "यह <strong>संज्ञेय</strong> अपराध है, इसलिए पुलिस बिना वारंट गिरफ्तारी कर सकती है।"
        if cognizable
        else "यह <strong>असंज्ञेय</strong> अपराध है, पुलिस को जांच के लिए मजिस्ट्रेट की अनुमति चाहिए।"
    )

    parts = [
        f"<strong>{name}</strong> भारतीय कानून की <strong>{section}</strong> के अंतर्गत आता है।",
        explanation,
        bail_text,
        cog_text,
        f"अधिकतम सजा: <strong>{max_pun}</strong>।",
    ]

    if checklist:
        title = checklist.get("title", "आपकी स्थिति")
        steps = checklist.get("immediate_steps", [])
        if steps:
            steps_str = ", ".join(steps[:3])
            parts.append(
                f"चूंकि स्थिति '<strong>{title}</strong>' है, तुरंत ये कदम उठाएं: {steps_str}।"
            )

    next_steps = law.get("next_2_hours", [])
    if next_steps:
        parts.append(
            f"अगले 2 घंटों में सबसे जरूरी कदम: <strong>{next_steps[0]}</strong>।"
        )

    parts.append(
        "याद रखें: हर गिरफ्तार व्यक्ति को 24 घंटे के भीतर मजिस्ट्रेट के सामने पेश करना अनिवार्य है और वकील का अधिकार है।"
    )

    return "<br><br>".join(parts)


# -----------------------------
# Chatbot Route
# -----------------------------
@app.post("/chatbot-guidance")
def chatbot_guidance(data: ChatbotInput):
    crime = data.crime
    situation = data.situation
    user_query = data.query.lower()

    law = laws_collection.find_one({"offence_key": crime}, {"_id": 0})

    checklist = None
    if situation:
        checklist = checklists_collection.find_one(
            {"situation_key": situation},
            {"_id": 0}
        )

    rights = list(rights_collection.find({}, {"_id": 0}))

    if not law:
        return {"reply": "I could not find legal guidance for this case."}

    if "overnight" in user_query or "24 hour" in user_query or "24 hours" in user_query:
        reply = "Police cannot keep an arrested person in custody for more than 24 hours without producing them before a magistrate."

    elif "bail" in user_query:
        if law.get("bailable"):
            reply = f"This appears to be a bailable offence under {law.get('section')}, so bail is generally possible."
        else:
            reply = f"This appears to be a non-bailable offence under {law.get('section')}, so bail is not automatic and usually requires court approval."

    elif "document" in user_query or "papers" in user_query:
        docs = law.get("documents_needed", [])
        if checklist and checklist.get("documents_needed"):
            docs = docs + checklist.get("documents_needed", [])
        docs = list(dict.fromkeys(docs))
        reply = "You should keep these documents ready: " + ", ".join(docs) + "."

    elif "lawyer" in user_query:
        reply = "The accused has the right to consult a lawyer, and the family should contact a lawyer immediately."

    elif "rights" in user_query:
        rights_list = [r["plain_text"] for r in rights[:3]]
        reply = "Important rights include: " + " ".join(rights_list)

    elif "police" in user_query and "can" in user_query:
        reply = "Police can: " + ", ".join(law.get("police_can_do", [])) + "."

    elif "police" in user_query and ("cannot" in user_query or "not" in user_query):
        reply = "Police cannot: " + ", ".join(law.get("police_cannot_do", [])) + "."

    else:
        reply = (
            f"This case appears to involve {law.get('offence_name')} under {law.get('section')}. "
            f"The immediate steps are: {', '.join(law.get('next_2_hours', [])[:2])}. "
            "For case-specific legal advice, a lawyer should be consulted."
        )

    return {"reply": reply}


# -----------------------------
# Serve Frontend (KEEP THIS LAST)
# -----------------------------
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")