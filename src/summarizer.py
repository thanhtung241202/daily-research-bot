import requests
import json
import os

class DeepSeekSummarizer:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
    
    def generate_summary(self, paper, difficulty):
        prompt = self._build_prompt(paper, difficulty)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": "Bạn là trợ lý học thuật chuyên tóm tắt research papers cho sinh viên Software Engineering."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"⚠️ Lỗi tóm tắt: {str(e)}"
    
    def _build_prompt(self, paper, difficulty):
        return f"""
Hãy tóm tắt research paper này cho sinh viên Software Engineering mới ra trường:

**TIÊU ĐỀ**: {paper['title']}
**TÁC GIẢ**: {', '.join(paper['authors'])}
**ABSTRACT**: {paper['abstract'][:1500]}...

YÊU CẦU:
1. Độ khó: {difficulty} - phù hợp với sinh viên SE
2. Định dạng:
   - 📌 **Tóm tắt ngắn** (3-4 câu)
   - 💡 **3 Key Insights** chính
   - 🤔 **1 Critical Thinking Question** để rèn tư duy phản biện
   - 🛠 **Application cho Software Engineering**

VIẾT BẰNG TIẾNG VIỆT (80%) và ENGLISH (20%) - giúp sinh viên làm quen với học thuật quốc tế.
"""