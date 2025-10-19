import os
import json
from datetime import datetime
from paper_fetcher import PaperFetcher
from summarizer import DeepSeekSummarizer
from pdf_builder import create_research_pdf
from email_sender import EmailSender

def main():
    print("🚀 Starting Daily Research Pipeline...")
    
    # Khởi tạo components
    fetcher = PaperFetcher()
    summarizer = DeepSeekSummarizer()
    email_sender = EmailSender()
    
    # Chọn chủ đề và độ khó ngẫu nhiên
    topic, difficulty = fetcher.get_random_topic_and_difficulty()
    print(f"🎯 Chủ đề: {topic} | Độ khó: {difficulty}")
    
    # Lấy paper từ arXiv
    paper = fetcher.fetch_paper_from_arxiv(topic)
    if not paper:
        print("❌ Không tìm thấy paper phù hợp")
        return
    
    print(f"📄 Paper: {paper['title'][:80]}...")
    
    # Tóm tắt với DeepSeek
    print("🤖 Đang tóm tết với DeepSeek...")
    summary = summarizer.generate_summary(paper, difficulty)
    
    # Tạo PDF
    pdf_filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf_path = create_research_pdf(paper, summary, difficulty, pdf_filename)
    print(f"📄 Đã tạo PDF: {pdf_filename}")
    
    # Gửi email
    print("📧 Đang gửi email...")
    success = email_sender.send_research_email(paper, summary, difficulty, pdf_path)
    
    if success:
        print("✅ Pipeline hoàn tất! Email đã được gửi.")
        # Lưu log
        save_sent_log(paper, difficulty)
    else:
        print("❌ Lỗi trong quá trình gửi email")

def save_sent_log(paper, difficulty):
    log_entry = {
        'date': datetime.now().isoformat(),
        'title': paper['title'],
        'category': paper['category'],
        'difficulty': difficulty,
        'arxiv_id': paper['arxiv_id']
    }
    
    try:
        with open('data/sent_papers.json', 'r+') as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except:
        with open('data/sent_papers.json', 'w') as f:
            json.dump([log_entry], f, indent=2)

if __name__ == "__main__":
    main()