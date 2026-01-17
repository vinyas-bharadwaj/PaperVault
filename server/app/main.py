from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .routers import uploads, auth, chatbot
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(chatbot.router)


@app.get("/")
def home():
    return {"Message": "Hello world!"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)