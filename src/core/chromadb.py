from langchain_chroma import Chroma
from src.config import CHROMA_DIR, EMBEDDING_MODEL
from langchain_ollama import OllamaEmbeddings
from . import library

ollama_ef = OllamaEmbeddings(
    model="embeddinggemma:latest"
)

collection_name = "docchat_collection"

def get_vectorStore():
     return Chroma(collection_name=collection_name, embedding_function=ollama_ef, persist_directory=CHROMA_DIR)

def add_chunks(chunks:list):
     client = get_vectorStore()
     ids = [chunk.metadata["chunk_id"] for chunk in chunks] # get the ids
     client.add_documents(documents=chunks, ids=ids) #insert the chunks with their ids

def delete_doc(doc_id):
     client = get_vectorStore()
     chunk_count = library.get_chunk_count(doc_id) #gets the counter
     if chunk_count == 0:
          return #if no chunks indexed just return
     chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(chunk_count)] # generate chunk ids in a list
     client.delete(ids=chunk_ids) #delete the chunks using the ids
     