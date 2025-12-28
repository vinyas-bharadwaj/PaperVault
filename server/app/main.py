from fastapi import FastAPI
import uvicorn
from routers import uploads

app = FastAPI()

app.include_router(uploads.router)


@app.get("/")
def home():
    return {"Message": "Hello world!"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)