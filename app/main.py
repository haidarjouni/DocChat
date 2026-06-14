from fastapi import FastAPI
from app.api.documents import router as documents
from app.api.chat import router as chat
app = FastAPI()

app.include_router(documents, tags=["documents"])
app.include_router(chat, tags=["chat"])

