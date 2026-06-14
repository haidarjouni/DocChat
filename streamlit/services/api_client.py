import httpx
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

async def fetch_documents():
     async with httpx.AsyncClient() as client:
          r = await client.get(f"{API_URL}/documents/")
          r.raise_for_status()
     return r.json()

async def send_message(payload):
     async with httpx.AsyncClient(timeout=900.0) as client:
        r = await client.post(f"{API_URL}/chat/message/", json=payload)
        r.raise_for_status()
     return r.json()

async def add_document(filename, file_bytes):
     async with httpx.AsyncClient(timeout=900.0) as client:
          files = {"file": (filename, file_bytes)}
          r = await client.post(f"{API_URL}/documents/upload/", files=files)
          r.raise_for_status()
     return r.json()
async def delete_document(doc_id):
     async with httpx.AsyncClient() as client:
          r = await client.delete(f"{API_URL}/documents/{doc_id}")
          r.raise_for_status()
     return r.json()

async def get_specific_document(doc_id):
     async with httpx.AsyncClient() as client:
          r = await client.get(f"{API_URL}/documents/{doc_id}")
          r.raise_for_status()
     return r.json()