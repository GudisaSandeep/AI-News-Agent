"""
Agent Module - Core AI News Agent Components

This module contains the main components of the AI News Agent:
- AINewsSearcher: News aggregation from multiple sources
- EmailSender: Email delivery functionality  
- AINewsAgent: Main orchestrator class
"""

from .ai_agent import AINewsAgent
from .news_searcher import AINewsSearcher
from .email_sender import EmailSender

__all__ = [
    "AINewsAgent",
    "AINewsSearcher",
    "EmailSender"
] 