"""
Settings Module

Configuration management for the AI News Agent.
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


def get_settings() -> Dict:
    """Get application settings from environment variables"""
    return {
        # Google Gemini API Configuration
        'gemini_api_key': os.getenv('GEMINI_API_KEY'),
        
        # Email Configuration
        'email_config': {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': os.getenv('SENDER_EMAIL'),
            'password': os.getenv('EMAIL_PASSWORD')
        },
        
        # Agent Configuration
        'recipient_email': os.getenv('RECIPIENT_EMAIL'),
        'run_mode': os.getenv('RUN_MODE', 'schedule').lower(),
        'schedule_time': os.getenv('SCHEDULE_TIME', '06:00'),
        'max_articles': int(os.getenv('MAX_ARTICLES', '10'))
    }


def validate_config() -> tuple[bool, Optional[str]]:
    """Validate that all required configuration is present"""
    settings = get_settings()
    
    required_fields = [
        ('gemini_api_key', 'GEMINI_API_KEY'),
        ('email_config.email', 'SENDER_EMAIL'),
        ('email_config.password', 'EMAIL_PASSWORD'),
        ('recipient_email', 'RECIPIENT_EMAIL')
    ]
    
    missing_fields = []
    
    for field_path, env_var in required_fields:
        # Navigate nested dictionaries
        value = settings
        for key in field_path.split('.'):
            value = value.get(key) if isinstance(value, dict) else None
            if value is None:
                break
        
        if not value:
            missing_fields.append(env_var)
    
    if missing_fields:
        error_msg = f"Missing required environment variables: {', '.join(missing_fields)}"
        return False, error_msg
    
    # Validate run mode
    if settings['run_mode'] not in ['once', 'schedule']:
        return False, "RUN_MODE must be either 'once' or 'schedule'"
    
    return True, None


def print_config_help():
    """Print helpful configuration instructions"""
    print("❌ Missing required environment variables!")
    print("\nPlease set these environment variables:")
    print("GEMINI_API_KEY - Your Google Gemini API key")
    print("SENDER_EMAIL - Your Gmail address")
    print("EMAIL_PASSWORD - Your Gmail App Password (not regular password)")
    print("RECIPIENT_EMAIL - Email address to send digest to")
    print("\n📧 Gmail Setup Instructions:")
    print("1. Enable 2-Factor Authentication on your Google account")
    print("2. Generate an App Password: https://myaccount.google.com/apppasswords")
    print("3. Use the 16-character app password as EMAIL_PASSWORD")