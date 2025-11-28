from typing import Dict, List

class ActionSuggester:
    def suggest(self, analysis: Dict[str, str]) -> List[str]:
        category = analysis.get("category", "general")

        suggestions = {
            "life_decision": [
                "Tell me more about your situation.",
                "What does your intuition say?",
                "What are you most afraid of?"
            ],
            "emotional": [
                "How long have you felt this way?",
                "What would help you feel safe?",
                "Share more about this feeling."
            ],
            "dharma": [
                "What feels like your calling?",
                "How can you serve better?",
                "What brings you joy?"
            ],
            "spiritual": [
                "What are you ready to release?",
                "How can I support your journey?",
                "What does your soul need?"
            ],
            "learning": [
                "What interests you most?",
                "How will you apply this?",
                "What questions remain?"
            ],
            "general": [
                "What's on your mind today?",
                "How can I guide you?",
                "Share your heart with me."
            ]
        }

        return suggestions.get(category, suggestions["general"])
