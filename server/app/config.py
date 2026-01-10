from qdrant_client.models import Distance, VectorParams
from google import genai
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

# Ensure collection exists
try:
    qdrant.create_collection(
        collection_name="papers",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
except:
    pass