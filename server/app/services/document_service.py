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
    def create_metadata(filename: str, title: str, semester: str, subject: str, professor: str | None, text: str, pdf_data: str = None) -> dict:
        """Create metadata dictionary for document"""
        metadata = {
            "filename": filename,
            "text": text,
            "title": title,
            "semester": semester,
            "subject": subject,
            "professor": professor
        }
        if pdf_data:
            metadata["pdf_data"] = pdf_data
        return metadata
    
    @staticmethod
    def format_search_result(result) -> dict:
        """Format search result for API response"""
        return {
            "doc_id": result.id,
            "title": result.payload.get("title", result.payload.get("filename", "Untitled")),
            "subject": result.payload.get("subject", "N/A"),
            "semester": result.payload.get("semester", "N/A"),
            "professor": result.payload.get("professor"),
            "text": result.payload.get("text", "")[:500],
            "score": result.score
        }
    
    @staticmethod
    def format_document(result) -> dict:
        """Format document for list view (no score)"""
        return {
            "doc_id": result.id,
            "title": result.payload.get("title", result.payload.get("filename", "Untitled")),
            "subject": result.payload.get("subject", "N/A"),
            "semester": result.payload.get("semester", "N/A"),
            "professor": result.payload.get("professor"),
            "text": result.payload.get("text", "")[:500],
            "score": 1.0  # Default score for list view
        }
    
    @staticmethod
    def format_document_with_pdf(result) -> dict:
        """Format document with full details including PDF data"""
        return {
            "doc_id": result.id,
            "title": result.payload.get("title", result.payload.get("filename", "Untitled")),
            "subject": result.payload.get("subject", "N/A"),
            "semester": result.payload.get("semester", "N/A"),
            "professor": result.payload.get("professor"),
            "filename": result.payload.get("filename", "document.pdf"),
            "text": result.payload.get("text", ""),
            "pdf_data": result.payload.get("pdf_data")
        }

document_service = DocumentService()
