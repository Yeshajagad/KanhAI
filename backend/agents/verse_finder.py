import json
from typing import Dict

class VerseFinder:
    def __init__(self, gita_data: Dict[str, Dict]):
        self.gita_data = gita_data

    def find(self, analysis: Dict[str, str]) -> Dict[str, str]:
        topic = analysis.get("topic", "duty")

        verse = self.gita_data.get(topic, self.gita_data.get("duty"))

        print(f"[MCP Tool] Verse Finder: Found BG {verse['chapter']}.{verse['verse_num']} for topic: {topic}")

        return verse
