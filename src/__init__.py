"""
AI News Agent - Source Package

A professional AI-powered news aggregation and email digest system.
"""

__version__ = "1.0.0"
__author__ = "AI News Agent Team"
__email__ = "contact@ainewsagent.com"

from src.agent.ai_agent import AINewsAgent
from src.agent.news_searcher import AINewsSearcher
from src.agent.email_sender import EmailSender

__all__ = [
    "AINewsAgent",
    "AINewsSearcher", 
    "EmailSender"
] 