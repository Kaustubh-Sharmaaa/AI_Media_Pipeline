import spacy
import re
from typing import Dict, Any

# Load spaCy English model (small, for speed)
nlp = spacy.load("en_core_web_sm")

# Example car makes and models for demo (expand as needed)
CAR_MAKES = ["Ford", "Toyota", "Honda", "BMW", "Audi"]
CAR_MODELS = ["Mustang GT", "Civic", "Corolla", "A4", "X5"]
COLORS = ["red", "blue", "black", "white", "silver", "green"]

# Simple intent/action keywords
ACTIONS = {
    "get_information": ["get information", "info", "details", "tell me about", "show me"],
    "book_test_drive": ["book test drive", "schedule test drive", "test drive"],
    "book_car": ["book", "reserve", "hold"],
}

def parse_intent(text: str) -> Dict[str, Any]:
    doc = nlp(text)
    params = {}
    # Extract car make
    for make in CAR_MAKES:
        if make.lower() in text.lower():
            params["car_make"] = make
            break
    # Extract car model
    for model in CAR_MODELS:
        if model.lower() in text.lower():
            params["car_model"] = model
            break
    # Extract color
    for color in COLORS:
        if color.lower() in text.lower():
            params["color"] = color
            break
    # Extract date (simple: look for 'yesterday', 'today', 'tomorrow', or DATE entities)
    date = None
    for token in doc:
        if token.lower_ in ["yesterday", "today", "tomorrow"]:
            date = token.text
            break
    if not date:
        for ent in doc.ents:
            if ent.label_ == "DATE":
                date = ent.text
                break
    if date:
        params["date"] = date
    # Extract intent/action
    intent = "unknown"
    lowered = text.lower()
    for act, keywords in ACTIONS.items():
        for kw in keywords:
            if kw in lowered:
                intent = act
                break
        if intent != "unknown":
            break
    # Fallback: if asking for info about a car, default to get_information
    if intent == "unknown" and ("information" in lowered or "details" in lowered or "tell me" in lowered):
        intent = "get_information"
    return {"intent": intent, "params": params}
