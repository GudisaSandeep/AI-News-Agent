# Setup Guide

This guide will walk you through setting up the AI News Agent on your system.

## Prerequisites

- Python 3.8 or higher
- Git
- Gmail account (for sending emails)
- Google Gemini API key

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-news-agent.git
cd ai-news-agent
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit the `.env` file with your credentials:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SENDER_EMAIL=your_gmail@gmail.com
   EMAIL_PASSWORD=your_gmail_app_password
   RECIPIENT_EMAIL=recipient@email.com
   RUN_MODE=once
   ```

## API Setup

### Google Gemini API

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key and set it as `GEMINI_API_KEY` in your `.env` file

### Gmail App Password

1. Enable 2-Factor Authentication on your Google account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use the 16-character password (remove spaces) as `EMAIL_PASSWORD`

## Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | - | ✅ |
| `SENDER_EMAIL` | Gmail address for sending | - | ✅ |
| `EMAIL_PASSWORD` | Gmail App Password | - | ✅ |
| `RECIPIENT_EMAIL` | Email to receive digest | - | ✅ |
| `RUN_MODE` | `once` or `schedule` | `schedule` | ❌ |
| `SCHEDULE_TIME` | Time for daily run (HH:MM) | `06:00` | ❌ |
| `MAX_ARTICLES` | Max articles per digest | `10` | ❌ |

## Testing the Setup

Run a one-time test to verify everything works:

```bash
# Set RUN_MODE=once in .env file first
python main.py
```

If successful, you should see:
- News articles being fetched
- AI summary being generated
- Email being sent to the recipient

## Troubleshooting

### Common Issues

**"Missing required environment variables"**
- Ensure all required variables are set in `.env`
- Check for typos in variable names

**"Email authentication failed"**
- Verify you're using an App Password, not your regular Gmail password
- Ensure 2-Factor Authentication is enabled
- Check that the email and password are correct

**"No news found"**
- Check your internet connection
- Verify RSS feeds are accessible
- Try running again later

**"API key error"**
- Verify your Gemini API key is valid
- Check API quotas and rate limits

### Getting Help

If you encounter issues:

1. Check the logs for error messages
2. Verify your `.env` file configuration
3. Test with `RUN_MODE=once` first
4. Check network connectivity

## Next Steps

Once setup is complete:
- Review the [Usage Guide](usage.md)
- Set up scheduling for daily delivery
- Customize news sources if needed 