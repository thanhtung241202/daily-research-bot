import google.generativeai as genai
import os
import requests

class GeminiSummarizer:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            print("⚠️ Chưa có GEMINI_API_KEY, sẽ dùng fallback summary")
    
    def generate_summary(self, paper, difficulty):
        prompt = self._build_prompt(paper, difficulty)
        
        try:
            print("🤖 Đang tóm tắt với Gemini...")
            response = self.model.generate_content(prompt)
            summary = response.text
            
            # Làm sạch kết quả
            summary = self._clean_summary(summary)
            print("✅ Tóm tắt thành công!")
            return summary
            
        except Exception as e:
            print(f"❌ Lỗi Gemini: {e}")
            return self._get_fallback_summary(paper, difficulty)
    
    def _build_prompt(self, paper, difficulty):
        return f"""
Bạn là trợ lý học thuật chuyên tóm tắt research papers cho sinh viên Công nghệ Phần mềm mới ra trường.

HÃY TÓM TẮT BÀI BÁO NÀY BẰNG TIẾNG VIỆT:

**TIÊU ĐỀ**: {paper['title']}
**TÁC GIẢ**: {', '.join(paper['authors'][:3])}
**TÓM TẮT GỐC**: {paper['abstract'][:1200]}...

YÊU CẦU:
- Độ khó: {difficulty} - phù hợp sinh viên mới ra trường
- VIẾT HOÀN TOÀN BẰNG TIẾNG VIỆT, tự nhiên, dễ hiểu
- Định dạng rõ ràng:

📌 TÓM TẮT CHÍNH: (3-4 câu giải thích nội dung chính)

💡 3 ĐIỂM QUAN TRỌNG:
1. [Ý chính 1 - giải thích rõ ràng]
2. [Ý chính 2 - liên quan đến software engineering]  
3. [Ý chính 3 - ứng dụng thực tế]

🤔 CÂU HỎI SUY NGẪM: [1 câu hỏi kích thích tư duy phản biện]

🛠 ỨNG DỤNG THỰC TẾ: [Cách áp dụng vào dự án phần mềm thực tế]

Lưu ý: Giữ nguyên các biểu tượng 📌💡🤔🛠 trong định dạng.
"""
    
    def _clean_summary(self, summary):
        """Làm sạch kết quả từ Gemini"""
        # Đảm bảo có đủ các phần
        if "📌" not in summary:
            summary = "📌 TÓM TẮT CHÍNH:\n" + summary
        
        # Giới hạn độ dài
        if len(summary) > 3000:
            summary = summary[:3000] + "..."
            
        return summary
    
    def _get_fallback_summary(self, paper, difficulty):
        """Fallback khi Gemini lỗi"""
        return f"""
📌 TÓM TẮT CHÍNH:
Bài báo "{paper['title']}" thuộc lĩnh vực {paper['category']}. Đây là nghiên cứu phù hợp cho sinh viên Công nghệ Phần mềm muốn tìm hiểu về ứng dụng thực tế.

💡 3 ĐIỂM QUAN TRỌNG:
1. Nghiên cứu cung cấp góc nhìn mới về {paper['category']}
2. Có thể ứng dụng trong phát triển phần mềm thực tế
3. Phù hợp với sinh viên mới ra trường muốn học hỏi

🤔 CÂU HỎI SUY NGẪM:
Làm thế nào để áp dụng ý tưởng từ nghiên cứu này vào dự án phần mềm của bạn?

🛠 ỨNG DỤNG THỰC TẾ:
Có thể sử dụng trong việc thiết kế kiến trúc hệ thống, cải thiện quy trình phát triển, hoặc tối ưu hiệu suất phần mềm.

📖 Đọc toàn văn: {paper['pdf_url']}
"""