from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException
from fastapi.responses import Response
from ..services import vector_service, embedding_service, document_service
import base64
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload(
    file: UploadFile = File(...),
    title: str = Form(...),
    semester: str = Form(...),
    subject: str = Form(...),
    professor: str = Form(None)
):
    # Extract text from PDF
    file_content = await file.read()
    text = document_service.extract_text_from_pdf(file_content)

    # Generate embedding
    embedding = embedding_service.generate_embedding(text)
    
    # Encode PDF as base64 for storage
    pdf_base64 = base64.b64encode(file_content).decode('utf-8')
    
    # Create metadata (now includes PDF file)
    metadata = document_service.create_metadata(
        filename=file.filename,
        title=title,
        semester=semester,
        subject=subject,
        professor=professor,
        text=text,
        pdf_data=pdf_base64
    )
    
    # Store in vector database
    doc_id = str(uuid.uuid4())  # Use UUID for unique ID
    vector_service.store_document(doc_id, embedding, metadata)
    
    return {"message": "uploaded", "title": title, "subject": subject, "doc_id": doc_id}

@router.post("/search")
async def search(query: str):
    # Generate query embedding
    query_vector = embedding_service.generate_embedding(query)
    
    # Search for similar documents
    results = vector_service.search_similar(query_vector, limit=5)
    
    # Format results
    return [document_service.format_search_result(r) for r in results]

@router.get("/documents")
async def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """List all documents with pagination"""
    # Get documents from vector database
    offset = (page - 1) * page_size
    results = vector_service.list_all_documents(limit=page_size, offset=offset)
    
    # Get total count
    total_count = vector_service.get_document_count()
    
    # Format results - use different format for list view (no score needed)
    documents = [document_service.format_document(r) for r in results]
    
    return {
        "documents": documents,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size
    }

@router.get("/document/{doc_id}")
async def view_document(doc_id: str):
    """Get a specific document by ID with PDF data"""
    document = vector_service.get_document_by_id(doc_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document_service.format_document_with_pdf(document)

@router.get("/document/{doc_id}/pdf")
async def get_pdf(doc_id: str):
    """Get the PDF file for a specific document"""
    document = vector_service.get_document_by_id(doc_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    pdf_base64 = document.payload.get("pdf_data")
    if not pdf_base64:
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    # Decode base64 to bytes
    pdf_bytes = base64.b64decode(pdf_base64)
    
    # Return PDF with proper headers
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{document.payload.get("filename", "document.pdf")}"'
        }
    )