from fpdf import FPDF
import os

class PDFBuilder(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Research Digest for Software Engineers', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def add_research_content(self, paper, summary, difficulty):
        # Tiêu đề
        self.set_font('Arial', 'B', 16)
        self.multi_cell(0, 10, paper['title'])
        self.ln(5)
        
        # Metadata
        self.set_font('Arial', 'I', 10)
        self.cell(0, 6, f"📚 Chủ đề: {paper['category']} | 🎯 Độ khó: {difficulty}")
        self.ln(8)
        
        # Nội dung tóm tắt
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 8, summary)
        
        # Link paper gốc
        self.ln(10)
        self.set_font('Arial', 'I', 10)
        self.multi_cell(0, 8, f"📄 Full paper: {paper['pdf_url']}")

def create_research_pdf(paper, summary, difficulty, output_path):
    pdf = PDFBuilder()
    pdf.add_page()
    pdf.add_research_content(paper, summary, difficulty)
    pdf.output(output_path)
    return output_path