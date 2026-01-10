from fastapi import APIRouter, UploadFile, File, Form
from PyPDF2 import PdfReader
from google import genai
from qdrant_client.models import PointStruct
from io import BytesIO
from config import qdrant, client

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload(
    file: UploadFile = File(...),
    title: str = Form(...),
    semester: str = Form(...),
    subject: str = Form(...),
    professor: str = Form(None)
):
    # Extract text
    pdf = PdfReader(BytesIO(await file.read()))
    text = " ".join(page.extract_text() for page in pdf.pages)

    # Generate embedding
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=[text]
    )
    embedding = response.embeddings[0].values
    
    # Store in Qdrant
    payload = {
        "filename": file.filename,
        "text": text,
        "title": title,
        "semester": semester,
        "subject": subject,
        "professor": professor
    }
    qdrant.upsert(
        collection_name="papers",
        points=[PointStruct(id=hash(file.filename), vector=embedding, payload=payload)]
    )
    
    return {"message": "uploaded", "title": title, "subject": subject}

@router.post("/search")
async def search(query: str):
    # Vectorize query
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=[query]
    )
    query_vector = response.embeddings[0].values
    
    # Search Qdrant
    results = qdrant.query_points(
        collection_name="papers",
        query=query_vector,
        limit=5
    ).points
    
    return [{
        "title": r.payload.get("title", r.payload.get("filename", "Untitled")),
        "subject": r.payload.get("subject", "N/A"),
        "semester": r.payload.get("semester", "N/A"),
        "professor": r.payload.get("professor"),
        "text": r.payload.get("text", "")[:500],
        "score": r.score
    } for r in results]