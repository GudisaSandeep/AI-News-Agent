"""
AI News Agent - Main Entry Point

This is the main script to run the AI News Agent application.
"""

import time
import schedule
from datetime import datetime

from src.agent.ai_agent import AINewsAgent
from src.config.settings import get_settings, validate_config, print_config_help


def send_daily_digest(agent: AINewsAgent, recipient_email: str):
    """Send daily digest wrapper function"""
    try:
        print(f"🌅 Daily digest triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        agent.generate_and_send_digest(recipient_email)
    except Exception as e:
        print(f"❌ Error in scheduled digest: {e}")


def main():
    """Main function to set up and run the AI news agent"""
    
    print("🤖 Starting AI News Agent...")
    
    # Get and validate configuration
    settings = get_settings()
    is_valid, error_msg = validate_config()
    
    if not is_valid:
        print_config_help()
        print(f"\n❌ Configuration Error: {error_msg}")
        return
    
    print(f"📧 Will send digest to: {settings['recipient_email']}")
    
    # Create AI agent
    try:
        agent = AINewsAgent(
            gemini_api_key=settings['gemini_api_key'],
            email_config=settings['email_config']
        )
        
        if settings['run_mode'] == 'once':
            # Option 1: Run once (for testing)
            print("📰 Generating AI news digest (one-time run)...")
            agent.generate_and_send_digest(settings['recipient_email'])
            
        else:
            # Option 2: Schedule daily emails
            schedule_time = settings['schedule_time']
            
            def scheduled_digest():
                send_daily_digest(agent, settings['recipient_email'])
            
            # Schedule daily digest
            schedule.every().day.at(schedule_time).do(scheduled_digest)
            
            print(f"⏰ AI News Agent scheduled to run daily at {schedule_time}")
            print("🔄 Service is running... Press Ctrl+C to stop")
            
            # Keep the script running
            while True:
                try:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
                except KeyboardInterrupt:
                    print("\n👋 AI News Agent stopped by user")
                    break
                except Exception as e:
                    print(f"❌ Scheduler error: {e}")
                    print("🔄 Continuing...")
                    time.sleep(300)  # Wait 5 minutes before retrying
        
    except Exception as e:
        print(f"❌ Error initializing AI agent: {e}")
        return


if __name__ == "__main__":
    # Install required packages first:
    # pip install -r requirements.txt
    main() 