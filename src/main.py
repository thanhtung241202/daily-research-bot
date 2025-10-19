import os
import json
import sys
from datetime import datetime
from paper_fetcher import PaperFetcher
from summarizer import GeminiSummarizer  # ĐÃ SỬA THÀNH GEMINI
from pdf_builder import create_pdf
from email_sender import EmailSender

def ensure_data_dir():
    if not os.path.exists('data'):
        os.makedirs('data')

def load_sent_papers():
    ensure_data_dir()
    try:
        with open('data/sent_papers.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_sent_paper(paper, difficulty):
    sent_papers = load_sent_papers()
    
    log_entry = {
        'date': datetime.now().isoformat(),
        'title': paper['title'],
        'category': paper['category'],
        'difficulty': difficulty,
        'arxiv_id': paper['arxiv_id']
    }
    
    sent_papers.append(log_entry)
    
    with open('data/sent_papers.json', 'w') as f:
        json.dump(sent_papers, f, indent=2)

def main():
    print("=" * 60)
    print("🚀 DAILY RESEARCH BOT - Starting Pipeline...")
    print("=" * 60)
    
    # Kiểm tra environment variables
    required_env_vars = ['GEMINI_API_KEY', 'SENDER_EMAIL', 'SENDER_PASSWORD', 'RECEIVER_EMAIL']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please set them in GitHub Secrets or .env file")
        sys.exit(1)
    
    # Khởi tạo components
    fetcher = PaperFetcher()
    summarizer = GeminiSummarizer()  # ĐÃ SỬA THÀNH GEMINI
    email_sender = EmailSender()
    
    # Chọn chủ đề và độ khó ngẫu nhiên
    topic, difficulty = fetcher.get_random_topic_and_difficulty()
    print(f"🎯 Chủ đề: {topic} | Độ khó: {difficulty}")
    
    # Lấy paper từ arXiv
    paper = fetcher.fetch_paper_from_arxiv(topic)
    if not paper:
        print("❌ Không tìm thấy paper phù hợp. Thoát...")
        return
    
    print(f"📄 Paper found: {paper['title'][:80]}...")
    
    # Tóm tắt với Gemini
    summary = summarizer.generate_summary(paper, difficulty)
    print("✅ Đã tạo tóm tắt")
    
    # Tạo PDF
    pdf_filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf_path = create_pdf(paper, summary, difficulty, pdf_filename)
    print(f"📄 Đã tạo PDF: {pdf_filename}")
    
    # Gửi email
    success = email_sender.send_email(paper, summary, difficulty, pdf_path)
    
    if success:
        print("🎉 Pipeline hoàn thành thành công!")
        save_sent_paper(paper, difficulty)
        
        # Clean up PDF file
        try:
            os.remove(pdf_path)
            print(f"🧹 Đã dọn dẹp: {pdf_filename}")
        except:
            pass
    else:
        print("❌ Pipeline thất bại ở bước gửi email")

if __name__ == "__main__":
    main()