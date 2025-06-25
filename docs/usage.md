# Usage Guide

This guide explains how to use the AI News Agent in different scenarios.

## Basic Usage

### One-Time Run

To generate and send a single news digest:

1. Set `RUN_MODE=once` in your `.env` file
2. Run the application:
   ```bash
   python main.py
   ```

This will:
- Fetch latest AI news from configured sources
- Generate an AI summary using Gemini
- Send an HTML email digest to the recipient

### Scheduled Daily Delivery

To set up automated daily news delivery:

1. Set `RUN_MODE=schedule` in your `.env` file
2. Optionally set `SCHEDULE_TIME=06:00` (24-hour format)
3. Run the application:
   ```bash
   python main.py
   ```

The agent will run continuously and send daily digests at the specified time.

## Running as a Service

### Windows (Task Scheduler)

1. Create a batch file `run_agent.bat`:
   ```batch
   @echo off
   cd /d "C:\path\to\ai-news-agent"
   venv\Scripts\activate
   python main.py
   ```

2. Use Task Scheduler to run the batch file at startup

### Linux/macOS (systemd/launchd)

Create a systemd service file `/etc/systemd/system/ai-news-agent.service`:

```ini
[Unit]
Description=AI News Agent
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/ai-news-agent
Environment=PATH=/path/to/ai-news-agent/venv/bin
ExecStart=/path/to/ai-news-agent/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable ai-news-agent
sudo systemctl start ai-news-agent
```

## Customization

### Adding News Sources

Edit `src/agent/news_searcher.py` to add new RSS feeds:

```python
self.news_sources = {
    'techcrunch_ai': 'https://techcrunch.com/category/artificial-intelligence/feed/',
    'ai_news': 'https://artificialintelligence-news.com/feed/',
    'your_source': 'https://your-news-site.com/ai/feed/',  # Add your source
}
```

### Customizing Email Templates

Modify the `_create_html_digest` method in `src/agent/ai_agent.py` to change:
- Email styling (CSS)
- Layout structure
- Content formatting

### Adjusting Article Limits

Set `MAX_ARTICLES` in your `.env` file:
```env
MAX_ARTICLES=15  # Default is 10
```

## API Integration

### Using as a Library

```python
from src.agent.ai_agent import AINewsAgent

# Initialize
agent = AINewsAgent(
    gemini_api_key="your-key",
    email_config={
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email': 'your@email.com',
        'password': 'app-password'
    }
)

# Generate and send digest
agent.generate_and_send_digest("recipient@email.com")
```

### Custom Workflow

```python
from src.agent.news_searcher import AINewsSearcher
from src.agent.email_sender import EmailSender

# Search for news
searcher = AINewsSearcher()
articles = searcher.search_rss_feeds(max_articles=5)

# Send custom email
sender = EmailSender("smtp.gmail.com", 587, "your@email.com", "password")
sender.send_email("recipient@email.com", "Subject", "HTML content")
```

## Monitoring and Logs

### Viewing Logs

The application prints status messages to the console:
- `🤖 Starting AI News Agent...`
- `📰 Generating AI news digest...`
- `📧 Email sent successfully...`

### Error Handling

Common error scenarios are handled gracefully:
- Network connectivity issues
- API rate limits
- Email authentication failures
- RSS feed parsing errors

## Advanced Configuration

### Environment Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `SCHEDULE_TIME` | `07:30` | Daily run time (24-hour format) |
| `MAX_ARTICLES` | `15` | Maximum articles per digest |
| `RUN_MODE` | `schedule` | `once` or `schedule` |

### News Source Configuration

The agent supports multiple news source types:
- RSS feeds
- Google News search
- Custom API endpoints (with code modifications)

### Email Configuration

Supports different SMTP providers:
- Gmail (default)
- Outlook/Hotmail
- Yahoo Mail
- Custom SMTP servers

Example for Outlook:
```env
# Use these settings in your email_config
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

## Best Practices

1. **Test First**: Always run with `RUN_MODE=once` before scheduling
2. **Monitor Quotas**: Check API usage to avoid rate limits
3. **Backup Configuration**: Keep your `.env` file secure and backed up
4. **Update Dependencies**: Regularly update packages for security
5. **Log Monitoring**: Check logs regularly for any issues

## Troubleshooting

### Performance Issues

- Reduce `MAX_ARTICLES` if emails are too large
- Check network latency to news sources
- Monitor API response times

### Email Delivery Issues

- Check spam folders
- Verify recipient email addresses
- Test with different email providers

### News Quality Issues

- Add more specific news sources
- Adjust the similarity threshold for duplicate detection
- Customize the AI summary prompt 