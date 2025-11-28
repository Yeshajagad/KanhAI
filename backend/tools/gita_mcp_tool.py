# ==================== tools/gita_mcp_tool.py ====================
"""
MCP Tool: Bhagavad Gita Database Interface
Implements Model Context Protocol for verse retrieval
"""

class GitaMCPTool:
    """
    MCP Tool for accessing Bhagavad Gita verses
    Follows Model Context Protocol specification
    """
    
    def __init__(self):
        self.tool_name = "gita_verse_finder"
        self.tool_description = "Search and retrieve relevant Bhagavad Gita verses"
        self.version = "1.0.0"
    
    def get_tool_schema(self) -> Dict:
        """MCP: Return tool schema for LLM"""
        return {
            "name": self.tool_name,
            "description": self.tool_description,
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to search (duty, fear, confusion, etc.)"
                    },
                    "context": {
                        "type": "string",
                        "description": "Additional context for search"
                    }
                },
                "required": ["topic"]
            }
        }
    
    def execute(self, topic: str, context: str = "") -> Dict:
        """
        MCP: Execute tool to retrieve verse
        
        This follows MCP protocol for tool execution
        """
        print(f"[MCP Tool] Executing: {self.tool_name} with topic='{topic}'")
        
        # In production, this would query vector database
        # For now, simple lookup
        verse_finder = VerseFinder()
        analysis = {'topic': topic}
        result = verse_finder.find_relevant_verse(analysis)
        
        return {
            "status": "success",
            "tool": self.tool_name,
            "result": result
        }


# ==================== database.py ====================
"""
SQLite Database for session management and memory
"""

import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import json

class Database:
    """SQLite database for persistent storage"""
    
    def __init__(self, db_path: str = "krishna_ai.db"):
        self.db_path = db_path
        self.conn = None
    
    def initialize(self):
        """Create tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                topics_discussed TEXT,
                emotional_state TEXT,
                message_count INTEGER DEFAULT 0,
                created_at TEXT,
                last_activity TEXT
            )
        ''')
        
        # Interactions table (conversation history)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                krishna_response TEXT,
                topic TEXT,
                emotion TEXT,
                verse_reference TEXT,
                timestamp TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')
        
        self.conn.commit()
        print("[Database] Initialized successfully")
    
    def save_interaction(self, interaction: Dict):
        """Save a conversation interaction"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO interactions 
            (session_id, user_message, krishna_response, topic, emotion, verse_reference, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            interaction['session_id'],
            interaction['user_message'],
            interaction['krishna_response'],
            interaction['topic'],
            interaction['emotion'],
            interaction['verse_reference'],
            interaction['timestamp']
        ))
        self.conn.commit()
    
    def get_session_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a session"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT user_message, krishna_response, topic, emotion, timestamp
            FROM interactions
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        return [
            {
                'user_message': row[0],
                'krishna_response': row[1],
                'topic': row[2],
                'emotion': row[3],
                'timestamp': row[4]
            }
            for row in rows
        ]
    
    def clear_session(self, session_id: str):
        """Clear all data for a session"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM interactions WHERE session_id = ?', (session_id,))
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        self.conn.commit()
    
    def count_total_messages(self) -> int:
        """Count total messages across all sessions"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM interactions')
        return cursor.fetchone()[0]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("[Database] Connection closed")


# ==================== utils/logger.py ====================
"""
Observability: Logging system for tracking agent activities
"""

import logging
from datetime import datetime

def setup_logger():
    """Configure logging for observability"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('krishna_ai.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('KrishnaAI')

def log_agent_activity(agent_name: str, activity: str):
    """Log agent activity for observability"""
    logger = logging.getLogger('KrishnaAI')
    logger.info(f"[{agent_name}] {activity}")


# ==================== utils/session_manager.py ====================
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
