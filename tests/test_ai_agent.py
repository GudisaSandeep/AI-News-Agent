"""
Unit tests for the main AI agent module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.agent.ai_agent import AINewsAgent


class TestAINewsAgent:
    """Test cases for AINewsAgent class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.gemini_api_key = "test-api-key"
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': 'test@gmail.com',
            'password': 'test_password'
        }
    
    @patch('src.agent.ai_agent.ChatGoogleGenerativeAI')
    @patch('src.agent.ai_agent.AINewsSearcher')
    @patch('src.agent.ai_agent.EmailSender')
    def test_init(self, mock_email_sender, mock_news_searcher, mock_llm):
        """Test initialization of AINewsAgent"""
        agent = AINewsAgent(self.gemini_api_key, self.email_config)
        
        # Verify components were initialized
        mock_llm.assert_called_once()
        mock_news_searcher.assert_called_once()
        mock_email_sender.assert_called_once_with(**self.email_config)
        
        # Verify tools were created
        assert len(agent.tools) == 2
        assert agent.tools[0].name == "search_ai_news"
        assert agent.tools[1].name == "format_news_digest"
    
    @patch('src.agent.ai_agent.ChatGoogleGenerativeAI')
    @patch('src.agent.ai_agent.AINewsSearcher')
    @patch('src.agent.ai_agent.EmailSender')
    def test_create_html_digest(self, mock_email_sender, mock_news_searcher, mock_llm):
        """Test HTML digest creation"""
        agent = AINewsAgent(self.gemini_api_key, self.email_config)
        
        # Test data
        articles = [
            {
                'title': 'Test AI News 1',
                'source': 'TechCrunch',
                'published': '2023-12-01 10:00',
                'summary': 'Test summary 1',
                'link': 'https://example.com/1'
            },
            {
                'title': 'Test AI News 2',
                'source': 'AI News',
                'published': '2023-12-01 11:00',
                'summary': 'Test summary 2',
                'link': 'https://example.com/2'
            }
        ]
        
        # Generate HTML
        html = agent._create_html_digest(articles)
        
        # Verify content
        assert 'AI News Daily Digest' in html
        assert 'Test AI News 1' in html
        assert 'Test AI News 2' in html
        assert 'TechCrunch' in html
        assert 'AI News' in html
        assert 'https://example.com/1' in html
        assert 'https://example.com/2' in html
    
    @patch('src.agent.ai_agent.ChatGoogleGenerativeAI')
    @patch('src.agent.ai_agent.AINewsSearcher')
    @patch('src.agent.ai_agent.EmailSender')
    def test_search_news_tool(self, mock_email_sender, mock_news_searcher, mock_llm):
        """Test news search tool wrapper"""
        # Mock news searcher
        mock_searcher_instance = mock_news_searcher.return_value
        mock_searcher_instance.search_rss_feeds.return_value = [
            {'title': 'RSS Article', 'source': 'RSS', 'published': '2023-12-01', 'summary': 'RSS summary', 'link': 'http://rss.com'}
        ]
        mock_searcher_instance.search_google_news.return_value = [
            {'title': 'Google Article', 'source': 'Google', 'published': '2023-12-01', 'summary': 'Google summary', 'link': 'http://google.com'}
        ]
        mock_searcher_instance.is_similar_title.return_value = False
        
        agent = AINewsAgent(self.gemini_api_key, self.email_config)
        
        # Test the tool
        result = agent._search_news_tool("test query")
        
        # Verify result is JSON string
        import json
        articles = json.loads(result)
        assert isinstance(articles, list)
        assert len(articles) == 2
    
    @patch('src.agent.ai_agent.ChatGoogleGenerativeAI')
    @patch('src.agent.ai_agent.AINewsSearcher')
    @patch('src.agent.ai_agent.EmailSender')
    def test_generate_and_send_digest_success(self, mock_email_sender, mock_news_searcher, mock_llm):
        """Test successful digest generation and sending"""
        # Mock components
        mock_searcher_instance = mock_news_searcher.return_value
        mock_searcher_instance.search_rss_feeds.return_value = [
            {'title': 'Test Article', 'source': 'Test', 'published': '2023-12-01', 'summary': 'Test summary', 'link': 'http://test.com'}
        ]
        mock_searcher_instance.search_google_news.return_value = []
        mock_searcher_instance.is_similar_title.return_value = False
        
        mock_sender_instance = mock_email_sender.return_value
        mock_sender_instance.send_email.return_value = True
        
        mock_llm_instance = mock_llm.return_value
        mock_response = Mock()
        mock_response.content = "This is an AI-generated summary."
        mock_llm_instance.invoke.return_value = mock_response
        
        agent = AINewsAgent(self.gemini_api_key, self.email_config)
        
        # Test the method
        agent.generate_and_send_digest("recipient@email.com")
        
        # Verify email was sent
        mock_sender_instance.send_email.assert_called_once()
        args = mock_sender_instance.send_email.call_args
        assert args[0][0] == "recipient@email.com"  # recipient
        assert "AI News Digest" in args[0][1]  # subject
        assert isinstance(args[0][2], str)  # HTML body
    
    @patch('src.agent.ai_agent.ChatGoogleGenerativeAI')
    @patch('src.agent.ai_agent.AINewsSearcher')
    @patch('src.agent.ai_agent.EmailSender')
    def test_generate_and_send_digest_no_articles(self, mock_email_sender, mock_news_searcher, mock_llm):
        """Test behavior when no articles are found"""
        # Mock empty results
        mock_searcher_instance = mock_news_searcher.return_value
        mock_searcher_instance.search_rss_feeds.return_value = []
        mock_searcher_instance.search_google_news.return_value = []
        
        mock_sender_instance = mock_email_sender.return_value
        
        agent = AINewsAgent(self.gemini_api_key, self.email_config)
        
        # Test the method
        agent.generate_and_send_digest("recipient@email.com")
        
        # Verify no email was sent
        mock_sender_instance.send_email.assert_not_called() 