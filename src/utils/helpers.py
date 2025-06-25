"""
Helper Functions Module

Utility functions used across the AI News Agent application.
"""

import re
from datetime import datetime
from typing import Optional


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters that might break email formatting
    text = text.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    
    return text


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if not text:
        return ""
    
    text = clean_text(text)
    
    if len(text) <= max_length:
        return text
    
    # Try to truncate at word boundary
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.7:  # If we can find a good word boundary
        truncated = truncated[:last_space]
    
    return truncated + suffix


def validate_email(email: str) -> bool:
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def safe_get_env(key: str, default: str = "", required: bool = False) -> str:
    """Safely get environment variable with validation"""
    import os
    
    value = os.getenv(key, default)
    
    if required and not value:
        raise ValueError(f"Required environment variable {key} is not set")
    
    return value