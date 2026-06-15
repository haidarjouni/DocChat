from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.core.exceptions import DocumentNotFoundError, DocumentAlreadyIndexedError, DocumentIndexingError
from ..storage import manifest_store
from ..storage.vectorstore import delete_doc as delete_vectors, add_chunks
from datetime import datetime
def index_pdf(doc_id):
     manifest = manifest_store.load_manifest() #load the manifest
     document = manifest["documents"].get(doc_id) #get the document using the doc_id
     if document is None :
          raise DocumentNotFoundError() #if the document doesn't exist or already indexed just return
     elif document.get("indexed_status") == "ok" and document.get("chunk_count", 0) > 0: #if already indexed do nothing
          raise DocumentAlreadyIndexedError()
     manifest_store.update_doc(doc_id, {
        "indexed_status": "indexing",
        "last_index_attempt": datetime.now().isoformat(),
        "index_error": None
     })
     try:    
          pages = load_pdf(doc_id, document) #load the pdf using the doc_id
          chunks = split_chunks(pages) #split it into chunks     
          delete_vectors(doc_id) #delete the old chunks if they exist
          add_chunks(chunks) # add the chunks to the vector store
          manifest_store.update_doc(doc_id, {
               "chunk_count": len(chunks),
               "indexed_status": "ok",
               "indexed_at": datetime.now().isoformat(),
               "index_error": None
          })
     except Exception as e:
          manifest_store.update_doc(doc_id, {
               "indexed_status": "failed",
               "index_error": str(e),
               "last_index_attempt": datetime.now().isoformat()
          })
          raise DocumentIndexingError(str(e))
     return True   
     
def load_pdf(doc_id, document):
     loader = PyPDFLoader(document.get("path")) #load the pdf using the path
     docs = loader.load() #load the pdf into a list of documents (one per page)
     for doc in docs:
          doc.metadata["doc_id"] = doc_id #foreach page/list add the doc_id to the metadata
          doc.metadata["filename"] = document.get("filename")
     return docs #return it   

def split_chunks(docs):
     text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP) #create the splitter
     texts = text_splitter.split_documents(docs) #split the documents into chunks and add them to the array
     for i, text in enumerate(texts): #foreach chunk add a unique chunk_id to the metadata using the doc_id and the chunk index
          text.metadata["chunk_id"] = f"{text.metadata.get('doc_id')}_chunk_{i}"
          text.metadata["chunk_index"] = i #add the chunk index to the metadata
     return texts