import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

class EmailSender:
    def __init__(self):
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
        self.receiver_email = RECEIVER_EMAIL
    
    def send_email(self, paper, summary, difficulty, pdf_path):
        # Tạo email message
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        
        # Subject tiếng Việt
        subject = f"🧠 {paper['category']} | {difficulty} | {paper['title'][:50]}..."
        message["Subject"] = subject
        
        # Email body HTML tiếng Việt
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }}
        .content {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .difficulty {{ display: inline-block; background: #28a745; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; }}
        .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; }}
        .section {{ margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🎯 Bản Tin Nghiên Cứu Hàng Ngày</h2>
            <p>Dành cho Kỹ sư Phần mềm 📚</p>
        </div>
        
        <div class="content">
            <div class="section">
                <p><strong>📖 Tiêu đề:</strong> {paper['title']}</p>
                <p><strong>🏷 Chủ đề:</strong> {paper['category']} | <span class="difficulty">🎯 {difficulty}</span></p>
                <p><strong>👨‍💻 Tác giả:</strong> {', '.join(paper['authors'][:3])}</p>
            </div>
            
            <hr>
            
            <div class="section" style="white-space: pre-line;">{summary}</div>
            
            <hr>
            
            <div class="section">
                <p><strong>🔗 Bài báo đầy đủ:</strong> <a href="{paper['pdf_url']}">{paper['pdf_url']}</a></p>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 Được tạo tự động bởi Research Bot | 💌 Phản hồi? Reply email này!</p>
        </div>
    </div>
</body>
</html>
"""
        
        message.attach(MIMEText(body_html, "html"))
        
        # Đính kèm PDF
        try:
            with open(pdf_path, "rb") as f:
                pdf_attach = MIMEApplication(f.read(), _subtype="pdf")
                pdf_attach.add_header('Content-Disposition', 'attachment', 
                                    filename=f"Research_{paper['category']}.pdf")
                message.attach(pdf_attach)
        except Exception as e:
            print(f"⚠️ Không thể đính kèm PDF: {e}")
        
        # Gửi email
        try:
            print("📧 Đang kết nối SMTP...")
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            print("✅ Email đã gửi thành công!")
            return True
        except Exception as e:
            print(f"❌ Lỗi gửi email: {e}")
            return False