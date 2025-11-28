"""
Configuration file for Krishna AI Agent
"""

import os
from dotenv import load_dotenv

load_dotenv()

# # API Keys (for production LLM integration)
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
# ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Database
DATABASE_PATH = 'krishna_ai.db'

# Server
HOST = '0.0.0.0'
PORT = 8000

# Logging
LOG_FILE = 'krishna_ai.log'
LOG_LEVEL = 'INFO'

# Agent Settings
MAX_CONVERSATION_HISTORY = 10
SESSION_TIMEOUT_HOURS = 24

# MCP Settings
MCP_TOOLS_ENABLED = True