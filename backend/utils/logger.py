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
