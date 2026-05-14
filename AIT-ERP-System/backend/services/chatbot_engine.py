import json
from pathlib import Path

KB_PATH = Path(__file__).resolve().parents[2] / "chatbot" / "knowledge_base.json"


class ChatbotEngine:
    def __init__(self):
        with open(KB_PATH, "r", encoding="utf-8") as f:
            self.kb = json.load(f)

    def reply(self, message: str) -> str:
        q = message.lower().strip()
        for entry in self.kb.get("intents", []):
            for kw in entry["keywords"]:
                if kw in q:
                    return entry["response"]
        return self.kb.get("fallback", "I couldn't find an answer. Please contact the admin office.")


engine = ChatbotEngine()