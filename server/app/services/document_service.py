from PyPDF2 import PdfReader
from io import BytesIO

class DocumentService:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text content from PDF file"""
        pdf = PdfReader(BytesIO(file_content))
        text = " ".join(page.extract_text() for page in pdf.pages)
        return text
    
    @staticmethod
    def create_metadata(filename: str, title: str, semester: str, subject: str, professor: str | None, text: str) -> dict:
        """Create metadata dictionary for document"""
        return {
            "filename": filename,
            "text": text,
            "title": title,
            "semester": semester,
            "subject": subject,
            "professor": professor
        }
    
    @staticmethod
    def format_search_result(result) -> dict:
        """Format search result for API response"""
        return {
            "title": result.payload.get("title", result.payload.get("filename", "Untitled")),
            "subject": result.payload.get("subject", "N/A"),
            "semester": result.payload.get("semester", "N/A"),
            "professor": result.payload.get("professor"),
            "text": result.payload.get("text", "")[:500],
            "score": result.score
        }

document_service = DocumentService()
