"""
Krishna AI Agent - Main FastAPI Server
Multi-agent system with MCP tools, session management, and observability
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime
import json

# ----------------- Load Gita JSON -----------------
with open("data/bhagvad_gita.json", "r") as f:
    gita_data = json.load(f)

# Import our agents
from agents.analyzer import InputAnalyzer
from agents.verse_finder import VerseFinder
from agents.krishna_ai import KrishnaAI
from agents.action_suggester import ActionSuggester

# Import tools and utilities
from tools.memory_tool import MemoryManager
from utils.logger import setup_logger, log_agent_activity
from utils.session_manager import SessionManager
from database import Database

# Initialize FastAPI app
app = FastAPI(title="Krishna AI Agent", version="1.0.0")


# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize logger (Observability)
logger = setup_logger()

# Initialize database
db = Database()

# Initialize all agents
analyzer = InputAnalyzer()
verse_finder = VerseFinder(gita_data)
krishna_ai = KrishnaAI()
action_suggester = ActionSuggester()

# Initialize tools
memory_manager = MemoryManager(db)
session_manager = SessionManager(db)

# ==================== REQUEST/RESPONSE MODELS ====================

class ChatRequest(BaseModel):
    """User chat message request"""
    user_id: str
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Krishna's response"""
    response: str
    verse: Optional[Dict] = None
    suggestions: List[str]
    session_id: str
    analysis: Dict

class SessionInfo(BaseModel):
    """Session information"""
    session_id: str
    user_id: str
    topics_discussed: List[str]
    emotional_state: str
    message_count: int
    created_at: str
    last_activity: str

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "active",
        "service": "Krishna AI Agent",
        "version": "1.0.0",
        "agents": ["Analyzer", "VerseFinder", "KrishnaAI", "ActionSuggester"]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - Sequential agent flow
    
    Flow:
    1. Agent 1: Analyze input
    2. Agent 2: Find relevant Gita verse (MCP Tool)
    3. Agent 3: Generate Krishna's response (LLM)
    4. Agent 4: Suggest follow-up actions
    """
    try:
        # Get or create session
        session_id = request.session_id or session_manager.create_session(request.user_id)
        session = session_manager.get_session(session_id)
        
        logger.info(f"[SESSION {session_id}] New message from user {request.user_id}")
        
        # ===== AGENT 1: ANALYZE INPUT =====
        log_agent_activity("Agent 1: Analyzer", "Starting analysis")
        analysis = analyzer.analyze(request.message)
        log_agent_activity("Agent 1: Analyzer", f"Detected: {analysis['topic']} ({analysis['emotion']})")
        
        # ===== AGENT 2: FIND VERSE (MCP TOOL) =====
        log_agent_activity("Agent 2: VerseFinder", "Searching Gita database via MCP")
        verse = verse_finder.find_relevant_verse(analysis)
        log_agent_activity("Agent 2: VerseFinder", f"Found BG {verse['chapter']}.{verse['verse_num']}")
        
        # ===== AGENT 3: GENERATE RESPONSE (LLM) =====
        log_agent_activity("Agent 3: KrishnaAI", "Generating divine guidance")
        
        # Get conversation history from memory
        history = memory_manager.get_conversation_history(session_id)
        
        # Generate Krishna's response
        response = await krishna_ai.generate_response(
            message=request.message,
            verse=verse,
            analysis=analysis,
            history=history
        )
        log_agent_activity("Agent 3: KrishnaAI", "Response generated successfully")
        
        # ===== AGENT 4: SUGGEST ACTIONS =====
        log_agent_activity("Agent 4: ActionSuggester", "Creating follow-up suggestions")
        suggestions = action_suggester.suggest_actions(analysis)
        
        # Save to memory (Long-term storage)
        memory_manager.save_interaction(
            session_id=session_id,
            user_message=request.message,
            krishna_response=response,
            analysis=analysis,
            verse=verse
        )
        
        # Update session state
        session_manager.update_session(
            session_id=session_id,
            topic=analysis['topic'],
            emotion=analysis['emotion']
        )
        
        logger.info(f"[SESSION {session_id}] Response delivered successfully")
        
        return ChatResponse(
            response=response,
            verse=verse,
            suggestions=suggestions,
            session_id=session_id,
            analysis=analysis
        )
        
    except Exception as e:
        logger.error(f"[ERROR] Chat endpoint failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str):
    """Get session information"""
    try:
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return SessionInfo(**session)
    except Exception as e:
        logger.error(f"[ERROR] Get session failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    """Get conversation history for a session"""
    try:
        history = memory_manager.get_conversation_history(session_id)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        logger.error(f"[ERROR] Get history failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a session (for testing or user reset)"""
    try:
        session_manager.delete_session(session_id)
        memory_manager.clear_session_memory(session_id)
        logger.info(f"[SESSION {session_id}] Cleared successfully")
        return {"status": "success", "message": "Session cleared"}
    except Exception as e:
        logger.error(f"[ERROR] Clear session failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    """Observability: Get system metrics"""
    try:
        total_sessions = session_manager.get_total_sessions()
        total_messages = memory_manager.get_total_messages()
        
        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "active_agents": 4,
            "mcp_tools": 2,
            "status": "operational"
        }
    except Exception as e:
        logger.error(f"[ERROR] Get metrics failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== STARTUP/SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Initialize database and agents on startup"""
    logger.info("🕉️  Krishna AI Agent starting up...")
    db.initialize()
    logger.info("✅ Database initialized")
    logger.info("✅ All agents ready")
    logger.info("✅ MCP tools loaded")
    logger.info("🙏 Krishna AI Agent is now active")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Krishna AI Agent shutting down...")
    db.close()
    logger.info("Namaste 🙏")

# ==================== RUN SERVER ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )