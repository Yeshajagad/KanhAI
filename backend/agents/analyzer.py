import re
from typing import Dict

class InputAnalyzer:
    def analyze(self, message: str) -> Dict[str, str]:
        msg = message.lower()

        if re.search(r"career|job|work|profession|confusion|choice", msg):
            return {"topic": "confusion", "emotion": "confused", "category": "life_decision"}

        if re.search(r"fear|afraid|scared|worry|anxious", msg):
            return {"topic": "fear", "emotion": "fearful", "category": "emotional"}

        if re.search(r"duty|responsibility|should|must|obligation", msg):
            return {"topic": "duty", "emotion": "burdened", "category": "dharma"}

        if re.search(r"attached|attachment|let go|holding", msg):
            return {"topic": "attachment", "emotion": "attached", "category": "spiritual"}

        if re.search(r"learn|knowledge|wisdom|understand", msg):
            return {"topic": "knowledge", "emotion": "curious", "category": "learning"}

        if re.search(r"stress|peace|calm|overwhelm", msg):
            return {"topic": "peace", "emotion": "stressed", "category": "emotional"}

        # Default case
        return {"topic": "duty", "emotion": "neutral", "category": "general"}
