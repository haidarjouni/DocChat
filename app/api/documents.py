from pypdf import PdfReader
from ..schema.documents import Document, DocumentDetail
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.core.exceptions import DocumentAlreadyIndexedError, DocumentIndexingError, DocumentNotFoundError, DuplicateDocumentError
from app.services.documents import remove_document, upload_document
from app.storage.manifest_store import list_documents, get_doc
router =  APIRouter(prefix="/api/v1/documents", tags=["documents"])

# upload and index documents
@router.post("/upload/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def upload_documents(file: UploadFile  = File()):
     if file is None:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded.")
     file_name = file.filename 

     header = await file.read(4) #reads the first bits of the file to check the signature
     
     if not header.startswith(b"%PDF") or not file_name.endswith(".pdf"):
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
               detail="File signature mismatch. The file content is not a valid PDF."
          ) #raise an error if the signature doesn't match the expected PDF signature or if the file extension is not .pdf
     await file.seek(0)  # Reset file pointer after reading header
     file_bytes = await file.read()
     try: #try uploading it 
          indexed = upload_document(file_name.strip(), file_bytes)
     except DocumentNotFoundError:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
     except DocumentAlreadyIndexedError:
          raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Document is already indexed.")
     except DocumentIndexingError:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during document indexing.")
     except DuplicateDocumentError:
          raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Document already exists.")
     except Exception as e:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
     finally:
          await file.close() #close file
     return { #return if it is successfully indexed
          "success": True,
          "doc_id": indexed["doc_id"], #id
          "filename": indexed["filename"], #name
          "indexed": indexed["indexed"] #  boolean if it is indexed or not
     }
     
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Document])
async def documents():
     return list_documents()

@router.get("/{doc_id}", status_code=status.HTTP_200_OK, response_model=DocumentDetail)
async def specific_document(doc_id: str):
     try:
          document = get_doc(doc_id)
          with open(document.get("path"), "rb") as f:
               reader = PdfReader(f)
               pages = len(reader.pages)
               text = reader.pages[0].extract_text() or ""
          document["pages"] = pages
          document["text"] = text[:2000]
     except DocumentNotFoundError:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
     except Exception as e:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
     return document

@router.delete("/{doc_id}", status_code=status.HTTP_200_OK, response_model=dict)
async def delete_document(doc_id: str):
     try:
          remove_document(doc_id)
     except DocumentNotFoundError:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
     except Exception as e:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
     return {"success": True, "message": f"Document with id {doc_id} has been deleted."}

