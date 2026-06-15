from langchain_chroma import Chroma
from app.core.config import CHROMA_DIR, EMBEDDING_MODEL
from langchain_ollama import OllamaEmbeddings
from . import manifest_store

# Shared embedding function used by Chroma for both indexing and retrieval.
ollama_ef = OllamaEmbeddings(
    model=EMBEDDING_MODEL
)

# Keep all document chunks in one named Chroma collection.
collection_name = "docchat_collection"


def get_vectorStore():
     # Create a Chroma client connected to the persistent local vector database.
     return Chroma(collection_name=collection_name, embedding_function=ollama_ef, persist_directory=CHROMA_DIR)


def add_chunks(chunks:list):
     client = get_vectorStore()

     # Use stable chunk IDs so chunks can be deleted or replaced later.
     ids = [chunk.metadata["chunk_id"] for chunk in chunks]

     client.add_documents(documents=chunks, ids=ids)


def delete_doc(doc_id):
     client = get_vectorStore()

     # The manifest tracks how many chunks were created for this document.
     chunk_count = manifest_store.get_chunk_count(doc_id)

     if chunk_count == 0:
          return True

     # Rebuild the same chunk IDs that were created during indexing.
     chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(chunk_count)]

     client.delete(ids=chunk_ids)
     return True