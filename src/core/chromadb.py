from langchain_chroma import Chroma
from src.config import CHROMA_DIR, EMBEDDING_MODEL
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from . import library

ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="embeddinggemma:latest",
)
collection_name = "docchat_collection"

def get_vectorStore():
     return Chroma(collection_name=collection_name, embedding_function=ollama_ef, persist_directory=CHROMA_DIR)

def add_chunks(chunks:list, collection=None):
     client = get_vectorStore()
     ids = [chunk.metadata["chunk_id"] for chunk in chunks]
     client.add(documents=chunks, ids=ids)

def delete_doc(doc_id, collection=None):
     client = get_vectorStore()
     chunk_count = library.get_chunk_count(doc_id)
     chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(chunk_count)]
     client.delete(ids=chunk_ids)
     