"""
Unit tests for the news searcher module.
"""

import pytest
from unittest.mock import Mock, patch
from src.agent.news_searcher import AINewsSearcher


class TestAINewsSearcher:
    """Test cases for AINewsSearcher class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.searcher = AINewsSearcher()
    
    def test_init(self):
        """Test initialization of AINewsSearcher"""
        assert isinstance(self.searcher.news_sources, dict)
        assert len(self.searcher.news_sources) > 0
        assert 'techcrunch_ai' in self.searcher.news_sources
    
    def test_is_similar_title(self):
        """Test title similarity detection"""
        title1 = "OpenAI releases new GPT model"
        title2 = "OpenAI releases new GPT model with improvements"
        title3 = "Apple announces new iPhone"
        
        # Similar titles should return True
        assert self.searcher.is_similar_title(title1, title2) == True
        
        # Different titles should return False
        assert self.searcher.is_similar_title(title1, title3) == False
    
    @patch('feedparser.parse')
    def test_search_rss_feeds_success(self, mock_parse):
        """Test successful RSS feed parsing"""
        # Mock feedparser response
        mock_entry = Mock()
        mock_entry.title = "Test AI News"
        mock_entry.link = "https://example.com/test"
        mock_entry.summary = "Test summary content"
        mock_entry.published_parsed = (2023, 12, 1, 10, 0, 0, 0, 0, 0)
        
        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        # Test the method
        articles = self.searcher.search_rss_feeds(max_articles=5)
        
        # Verify results
        assert isinstance(articles, list)
        # Should have called parse for each news source
        assert mock_parse.call_count == len(self.searcher.news_sources)
    
    @patch('feedparser.parse')
    def test_search_rss_feeds_error_handling(self, mock_parse):
        """Test RSS feed error handling"""
        # Simulate parse error
        mock_parse.side_effect = Exception("Network error")
        
        # Should not raise exception
        articles = self.searcher.search_rss_feeds()
        assert isinstance(articles, list)
    
    @patch('feedparser.parse')
    def test_search_google_news(self, mock_parse):
        """Test Google News search"""
        # Mock feedparser response
        mock_entry = Mock()
        mock_entry.title = "Google News AI Article"
        mock_entry.link = "https://news.google.com/test"
        mock_entry.summary = "Google news summary"
        mock_entry.published = "2023-12-01"
        
        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        # Test the method
        articles = self.searcher.search_google_news(max_results=3)
        
        # Verify results
        assert isinstance(articles, list)
        mock_parse.assert_called_once()
    
    def test_search_google_news_error_handling(self):
        """Test Google News error handling"""
        with patch('feedparser.parse', side_effect=Exception("Error")):
            articles = self.searcher.search_google_news()
            assert isinstance(articles, list)
            assert len(articles) == 0 