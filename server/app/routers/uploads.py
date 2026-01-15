from fastapi import APIRouter, UploadFile, File, Form
from ..services import vector_service, embedding_service, document_service

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
    
    # Create metadata
    metadata = document_service.create_metadata(
        filename=file.filename,
        title=title,
        semester=semester,
        subject=subject,
        professor=professor,
        text=text
    )
    
    # Store in vector database
    doc_id = hash(file.filename)
    vector_service.store_document(doc_id, embedding, metadata)
    
    return {"message": "uploaded", "title": title, "subject": subject}

@router.post("/search")
async def search(query: str):
    # Generate query embedding
    query_vector = embedding_service.generate_embedding(query)
    
    # Search for similar documents
    results = vector_service.search_similar(query_vector, limit=5)
    
    # Format results
    return [document_service.format_search_result(r) for r in results]