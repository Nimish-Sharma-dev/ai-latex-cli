import json
from pathlib import Path

# Navigate up one level to project root, then into templates/
INTENTS_JSON_PATH = Path(__file__).resolve().parents[2] / "templates" / "intents.json"

def parse_intent(prompt: str) -> str:
    """
    Scans the prompt text for keywords defined in templates/intents.json.
    Returns the matching intent key, or 'standard' if no keywords match.
    """
    p_lower = prompt.lower()
    
    if not INTENTS_JSON_PATH.exists():
        return "standard"
        
    try:
        with open(INTENTS_JSON_PATH, "r", encoding="utf-8") as f:
            intents_data = json.load(f)
    except json.JSONDecodeError:
        return "standard"

    # Search for a matching keyword
    for intent, keywords in intents_data.items():
        if any(keyword in p_lower for keyword in keywords):
            return intent
            
    return "standard"