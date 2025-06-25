# 🤖 AI News Agent

An intelligent news aggregation and email digest system that automatically searches, summarizes, and delivers the latest AI news to your inbox using Google's Gemini AI.

# Demo Video
[![Demo Video](https://your-thumbnail-link.jpg)](docs/News Agent - Made with Clipchamp.mp4)

## ✨ Features

- **Multi-Source News Aggregation**: Fetches AI news from TechCrunch, AI News, VentureBeat, MIT Technology Review, and Google News
- **AI-Powered Summaries**: Uses Google's Gemini AI to generate executive summaries of news trends
- **Automated Email Delivery**: Sends beautifully formatted HTML email digests
- **Smart Duplicate Detection**: Removes duplicate articles across sources
- **Flexible Scheduling**: Run once or schedule daily delivery
- **Professional HTML Templates**: Clean, responsive email design

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Gmail account (for sending emails)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GudisaSandeep/AI-News-Agent
   cd AI-News-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your credentials:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SENDER_EMAIL=your_gmail@gmail.com
   EMAIL_PASSWORD=your_gmail_app_password
   RECIPIENT_EMAIL=recipient@email.com
   RUN_MODE=once  # or 'schedule' for daily delivery
   ```

4. **Run the agent**
   ```bash
   python main.py
   ```

## 📧 Gmail Setup

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Use the 16-character app password (not your regular Gmail password)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | ✅ |
| `SENDER_EMAIL` | Gmail address for sending emails | ✅ |
| `EMAIL_PASSWORD` | Gmail App Password | ✅ |
| `RECIPIENT_EMAIL` | Email to receive the digest | ✅ |
| `RUN_MODE` | `once` for single run, `schedule` for daily | ❌ |

### News Sources

The agent fetches news from:
- TechCrunch AI
- Artificial Intelligence News
- VentureBeat AI
- MIT Technology Review
- Google News

## 📁 Project Structure

```
ai-news-agent/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── main.py                  # Application entry point
├── src/                     # Source code
│   ├── agent/              # Core agent modules
│   │   ├── news_searcher.py # News aggregation logic
│   │   ├── email_sender.py  # Email sending functionality
│   │   └── ai_agent.py     # Main AI agent class
│   ├── config/             # Configuration management
│   │   └── settings.py     # Settings and constants
│   └── utils/              # Utility functions
│       └── helpers.py      # Helper functions
├── tests/                  # Unit tests
└── docs/                   # Additional documentation
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📖 Usage Examples

### One-time Run
```bash
# Set RUN_MODE=once in .env
python main.py
```

### Scheduled Daily Delivery
```bash
# Set RUN_MODE=schedule in .env (default)
python main.py
# Runs daily at 6:00 AM
```

### Custom Integration
```python
from src.agent.ai_agent import AINewsAgent

# Initialize agent
agent = AINewsAgent(gemini_api_key, email_config)

# Generate and send digest
agent.generate_and_send_digest("recipient@email.com")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚨 Troubleshooting

### Common Issues

**Email Authentication Failed**
- Ensure you're using an App Password, not your regular Gmail password
- Verify 2-Factor Authentication is enabled
- Check that the email and password are correct in `.env`

**No News Found**
- Check your internet connection
- Verify RSS feeds are accessible
- Try running in 'once' mode first for testing

**API Errors**
- Verify your Gemini API key is valid
- Check API quotas and limits

## 🔗 Links

- [Google Gemini API](https://ai.google.dev/)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)
- [LangChain Documentation](https://langchain.readthedocs.io/)

## 💡 Roadmap

- [ ] Add more news sources
- [ ] Support for custom news categories
- [ ] Web dashboard interface
- [ ] Slack/Discord integration
- [ ] Custom email templates
- [ ] News sentiment analysis 
