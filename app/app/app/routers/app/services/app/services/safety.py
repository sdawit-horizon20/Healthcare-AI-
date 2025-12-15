EMERGENCY_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "severe bleeding",
    "loss of consciousness"
]

def is_emergency(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in EMERGENCY_KEYWORDS)

def disclaimer():
    return "\n\n⚠️ This AI provides general health information only."
