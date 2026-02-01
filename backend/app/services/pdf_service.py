"""
Service for extracting text from PDF files
"""
from PyPDF2 import PdfReader
from io import BytesIO
from typing import BinaryIO


class PDFExtractionService:
    """
    Service class for PDF text extraction operations
    """
    
    @staticmethod
    def extract_text_from_pdf(pdf_file: BinaryIO) -> str:
        """
        Extract text content from a PDF file
        
        Args:
            pdf_file: Binary file object containing PDF data
            
        Returns:
            str: Extracted text from all pages of the PDF
            
        Raises:
            Exception: If PDF reading or text extraction fails
        """
        try:
            # Read the PDF file
            pdf_reader = PdfReader(pdf_file)
            
            # Extract text from all pages
            extracted_text = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
            
            # Join all page texts with newlines
            full_text = "\n".join(extracted_text)
            
            return full_text
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def validate_pdf_file(file_content: bytes) -> bool:
        """
        Validate if the uploaded file is a valid PDF
        
        Args:
            file_content: Binary content of the file
            
        Returns:
            bool: True if valid PDF, False otherwise
        """
        try:
            # Check PDF header signature
            if file_content[:4] == b'%PDF':
                return True
            return False
        except Exception:
            return False
