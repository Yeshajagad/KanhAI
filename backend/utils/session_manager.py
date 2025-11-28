"""
Session & State Management
"""

import uuid
from datetime import datetime
from typing import Dict, Optional
import json

class SessionManager:
    """Manages user sessions and state"""
    
    def __init__(self, database):
        self.db = database
    
    def create_session(self, user_id: str) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        
        cursor = self.db.conn.cursor()
        cursor.execute('''
            INSERT INTO sessions 
            (session_id, user_id, topics_discussed, emotional_state, created_at, last_activity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            user_id,
            json.dumps([]),
            'neutral',
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        self.db.conn.commit()
        
        print(f"[SessionManager] Created session {session_id} for user {user_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session information"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT session_id, user_id, topics_discussed, emotional_state, 
                   message_count, created_at, last_activity
            FROM sessions WHERE session_id = ?
        ''', (session_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return {
            'session_id': row[0],
            'user_id': row[1],
            'topics_discussed': json.loads(row[2]),
            'emotional_state': row[3],
            'message_count': row[4],
            'created_at': row[5],
            'last_activity': row[6]
        }
    
    def update_session(self, session_id: str, topic: str, emotion: str):
        """Update session with new interaction"""
        session = self.get_session(session_id)
        if not session:
            return
        
        # Update topics
        topics = session['topics_discussed']
        if topic not in topics:
            topics.append(topic)
        
        cursor = self.db.conn.cursor()
        cursor.execute('''
            UPDATE sessions 
            SET topics_discussed = ?,
                emotional_state = ?,
                message_count = message_count + 1,
                last_activity = ?
            WHERE session_id = ?
        ''', (
            json.dumps(topics),
            emotion,
            datetime.now().isoformat(),
            session_id
        ))
        self.db.conn.commit()
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        cursor = self.db.conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        self.db.conn.commit()
        print(f"[SessionManager] Deleted session {session_id}")
    
    def get_total_sessions(self) -> int:
        """Get total number of sessions"""
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM sessions')
        return cursor.fetchone()[0]
