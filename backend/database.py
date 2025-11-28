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

