"""
Resume Parser Module
Extracts text and metadata from PDF resumes
"""
import PyPDF2
import pdfplumber
import re
from typing import Dict, Optional


class ResumeParser:
    """Parse resume PDFs and extract text content"""
    
    def __init__(self):
        self.text = ""
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using pdfplumber as primary method"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Fallback to PyPDF2 if pdfplumber fails
            if not text.strip():
                text = self._extract_with_pypdf2(pdf_path)
            
            self.text = text
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Fallback method using PyPDF2"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error with PyPDF2 extraction: {str(e)}")
        return text
    
    def extract_email(self, text: Optional[str] = None) -> Optional[str]:
        """Extract email address from text"""
        text = text or self.text
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def extract_phone(self, text: Optional[str] = None) -> Optional[str]:
        """Extract phone number from text"""
        text = text or self.text
        # Match various phone formats
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None
    
    def extract_name(self, text: Optional[str] = None) -> Optional[str]:
        """Extract candidate name (usually first line or two)"""
        text = text or self.text
        lines = text.strip().split('\n')
        # Typically name is in the first few lines
        if lines:
            return lines[0].strip()
        return None
    
    def parse(self, pdf_path: str) -> Dict[str, str]:
        """Parse resume and extract all information"""
        text = self.extract_text_from_pdf(pdf_path)
        
        return {
            "text": text,
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text)
        }
