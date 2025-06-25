"""
News Searcher Module

Handles news aggregation from multiple sources including RSS feeds and Google News.
"""

import urllib.parse
from datetime import datetime, timedelta
from typing import List, Dict
import feedparser


class AINewsSearcher:
    """Tool for searching AI news from multiple sources"""
    
    def __init__(self):
        self.news_sources = {
            'techcrunch_ai': 'https://techcrunch.com/category/artificial-intelligence/feed/',
            'ai_news': 'https://artificialintelligence-news.com/feed/',
            'venturebeat_ai': 'https://venturebeat.com/ai/feed/',
            'mit_tech_ai': 'https://www.technologyreview.com/topic/artificial-intelligence/feed/',
        }
    
    def search_rss_feeds(self, max_articles: int = 10) -> List[Dict]:
        """Search AI news from RSS feeds"""
        articles = []
        
        for source_name, feed_url in self.news_sources.items():
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:max_articles//len(self.news_sources)]:
                    # Get articles from last 24 hours
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                        if pub_date > datetime.now() - timedelta(days=1):
                            articles.append({
                                'title': entry.title,
                                'link': entry.link,
                                'summary': entry.get('summary', '')[:200] + '...',
                                'source': source_name,
                                'published': pub_date.strftime('%Y-%m-%d %H:%M')
                            })
                    else:
                        # If no published date, include recent articles anyway
                        articles.append({
                            'title': entry.title,
                            'link': entry.link,
                            'summary': entry.get('summary', '')[:200] + '...',
                            'source': source_name,
                            'published': 'Recent'
                        })
            except Exception as e:
                print(f"Error fetching from {source_name}: {e}")
        
        return sorted(articles, key=lambda x: x['published'], reverse=True)[:max_articles]
    
    def search_google_news(self, query: str = "artificial intelligence", max_results: int = 5) -> List[Dict]:
        """Search Google News for AI articles (alternative method)"""
        # Note: For production, consider using Google News API or News API
        articles = []
        try:
            # URL encode the query to handle spaces and special characters
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en&gl=US&ceid=US:en"
            
            print(f"Fetching from Google News: {search_url}")
            feed = feedparser.parse(search_url)
            
            for entry in feed.entries[:max_results]:
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.get('summary', '')[:200] + '...',
                    'source': 'Google News',
                    'published': entry.get('published', 'Recent')
                })
        except Exception as e:
            print(f"Error fetching from Google News: {e}")
        
        return articles
    
    def is_similar_title(self, title1: str, title2: str) -> bool:
        """Check if two titles are similar (basic duplicate detection)"""
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        common_words = words1.intersection(words2)
        return len(common_words) > len(words1) * 0.6  # 60% similarity threshold 