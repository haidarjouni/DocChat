from fastapi import FastAPI
from app.api.documents import router as documents
app = FastAPI()

app.include_router(documents, tags=["documents"])
