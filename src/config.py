import os

# AI API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Email Configuration
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD') 
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

# Research Categories
RESEARCH_CATEGORIES = {
    'Software Engineering': ['cs.SE', 'cs.PL'],
    'Machine Learning': ['cs.LG', 'cs.AI', 'stat.ML'],
    'HCI': ['cs.HC', 'cs.HCI'],
    'Algorithms': ['cs.DS', 'cs.CC'],
    'Emerging Tech': ['cs.CY', 'cs.ETC', 'cs.CR']
}

DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard']
