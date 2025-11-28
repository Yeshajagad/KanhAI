"""
Memory Tool: Manages conversation history and long-term memory
"""

from typing import List, Dict, Optional
from datetime import datetime
import json

class MemoryManager:
    """Manages session memory and conversation history"""
    
    def __init__(self, database):
        self.db = database
    
    def save_interaction(self, session_id: str, user_message: str,
                        krishna_response: str, analysis: Dict, verse: Dict):
        """Save a conversation interaction to memory"""
        interaction = {
            'session_id': session_id,
            'user_message': user_message,
            'krishna_response': krishna_response,
            'topic': analysis['topic'],
            'emotion': analysis['emotion'],
            'verse_reference': f"BG {verse['chapter']}.{verse['verse_num']}",
            'timestamp': datetime.now().isoformat()
        }
        
        self.db.save_interaction(interaction)
        print(f"[Memory] Saved interaction for session {session_id}")
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve conversation history for context"""
        return self.db.get_session_history(session_id, limit)
    
    def clear_session_memory(self, session_id: str):
        """Clear all memory for a session"""
        self.db.clear_session(session_id)
        print(f"[Memory] Cleared session {session_id}")
    
    def get_total_messages(self) -> int:
        """Get total message count across all sessions"""
        return self.db.count_total_messages()
