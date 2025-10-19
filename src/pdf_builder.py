from fpdf import FPDF
from datetime import datetime
import re

class ResearchPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'Research Digest for Software Engineers', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 8, f'Generated on {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def clean_text(self, text):
        """Loại bỏ tất cả emoji và ký tự đặc biệt không hỗ trợ"""
        if not text:
            return ""
        
        # Loại bỏ emoji và ký tự đặc biệt
        cleaned = re.sub(r'[^\x00-\x7F]+', ' ', text)
        
        # Thay thế các ký tự đặc biệt cụ thể
        replacements = {
            '📌': '>>',
            '💡': '->',
            '🤔': '??',
            '🛠': '=>',
            '📚': '[TOPIC]',
            '🎯': '[DIFFICULTY]',
            '👨‍💻': '[AUTHOR]',
            '📄': '[PAPER]',
            '🔗': '[LINK]',
            '⚠': '[NOTE]',
            '✅': '[DONE]',
            '❌': '[ERROR]',
            '🚀': '[START]'
        }
        
        for char, replacement in replacements.items():
            cleaned = cleaned.replace(char, replacement)
        
        return cleaned.strip()
    
    def add_content(self, paper, summary, difficulty):
        # Tiêu đề paper
        self.set_font('Helvetica', 'B', 14)
        title = self.clean_text(paper['title'])
        self.multi_cell(0, 8, title)
        self.ln(5)
        
        # Metadata
        self.set_font('Helvetica', 'I', 10)
        metadata = f"TOPIC: {paper['category']} | DIFFICULTY: {difficulty}"
        self.cell(0, 6, metadata)
        self.ln(8)
        
        # Tác giả
        authors = ', '.join(paper['authors'][:3])
        self.cell(0, 6, f"AUTHORS: {authors}")
        self.ln(10)
        
        # Nội dung tóm tắt (đã làm sạch)
        self.set_font('Helvetica', '', 12)
        clean_summary = self.clean_text(summary)
        
        # Chia thành các đoạn và xử lý
        paragraphs = clean_summary.split('\n')
        for para in paragraphs:
            if para.strip():
                # Xử lý các heading đặc biệt
                if para.startswith('>>') or para.startswith('->') or para.startswith('??') or para.startswith('=>'):
                    self.set_font('Helvetica', 'B', 12)
                    self.multi_cell(0, 8, para)
                    self.set_font('Helvetica', '', 12)
                else:
                    self.multi_cell(0, 8, para)
                self.ln(4)
        
        self.ln(10)
        
        # Link paper gốc
        self.set_font('Helvetica', 'I', 10)
        self.multi_cell(0, 8, f"FULL PAPER: {paper['pdf_url']}")

def create_pdf(paper, summary, difficulty, filename="research_digest.pdf"):
    try:
        pdf = ResearchPDF()
        pdf.add_page()
        pdf.add_content(paper, summary, difficulty)
        pdf.output(filename)
        print(f"✅ PDF created successfully: {filename}")
        return filename
    except Exception as e:
        print(f"❌ PDF creation failed: {e}")
        # Fallback: tạo file text thay vì PDF
        txt_filename = filename.replace('.pdf', '.txt')
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(f"Research Digest\\n")
            f.write(f"Title: {paper['title']}\\n")
            f.write(f"Topic: {paper['category']} | Difficulty: {difficulty}\\n")
            f.write(f"Authors: {', '.join(paper['authors'][:3])}\\n\\n")
            f.write(summary)
            f.write(f"\\n\\nFull Paper: {paper['pdf_url']}\\n")
        print(f"✅ Created fallback text file: {txt_filename}")
        return txt_filename