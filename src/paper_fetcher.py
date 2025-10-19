import feedparser
import random
import requests
from datetime import datetime

class PaperFetcher:
    def __init__(self):
        self.categories = {
            'Software Engineering': ['cs.SE', 'cs.PL'],
            'Machine Learning': ['cs.LG', 'cs.AI', 'stat.ML'],
            'HCI': ['cs.HC', 'cs.HCI'],
            'Algorithms': ['cs.DS', 'cs.CC'],
            'Emerging Tech': ['cs.CY', 'cs.ETC', 'cs.CR']
        }
        
        self.difficulty_levels = ['Easy', 'Medium', 'Hard']
    
    def get_random_topic_and_difficulty(self):
        topic = random.choice(list(self.categories.keys()))
        difficulty = random.choice(self.difficulty_levels)
        return topic, difficulty
    
    def fetch_paper_from_arxiv(self, topic):
        categories = self.categories[topic]
        category = random.choice(categories)
        
        # Tìm papers có từ khóa "survey", "review", "tutorial"
        query = "survey+OR+review+OR+tutorial+OR+overview"
        url = f"http://export.arxiv.org/api/query?search_query=cat:{category}+AND+({query})&start=0&max_results=50"
        
        feed = feedparser.parse(url)
        
        if len(feed.entries) == 0:
            return None
        
        # Lọc papers có abstract đầy đủ
        valid_entries = [entry for entry in feed.entries if len(entry.summary) > 500]
        
        if not valid_entries:
            return None
            
        paper = random.choice(valid_entries)
        
        return {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'abstract': paper.summary,
            'pdf_url': next(link.href for link in paper.links if link.type == 'application/pdf'),
            'published': paper.published,
            'arxiv_id': paper.id.split('/abs/')[-1],
            'category': topic
        }