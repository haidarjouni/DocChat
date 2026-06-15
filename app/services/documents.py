from ..storage.manifest_store import add_upload
from ..rag.indexer import index_pdf
from ..storage.manifest_store import delete_doc as remove_from_library
from ..storage.vectorstore import delete_doc as remove_from_vectorstore
def upload_document(filename, file_bytes):
     doc_id = add_upload(filename, file_bytes) #add the document to the library and get the doc_id
     return {
          "success": True,
          "doc_id": doc_id,
          "filename": filename,
          "indexed":  index_pdf(doc_id)
     } # returns if the indexed file worked or not
     
def remove_document(doc_id: str):
     remove_from_vectorstore(doc_id)
     remove_from_library(doc_id)
     return True