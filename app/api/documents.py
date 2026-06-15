from pypdf import PdfReader
from ..schema.documents import Document, DocumentDetail
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.core.exceptions import DocumentAlreadyIndexedError, DocumentIndexingError, DocumentNotFoundError, DuplicateDocumentError
from app.services.documents import remove_document, upload_document
from app.storage.manifest_store import list_documents, get_doc

# Group all document-related endpoints under a single router.
router =  APIRouter(prefix="/api/v1/documents", tags=["documents"])


# Upload a PDF, validate it, store it, and index it for retrieval.
@router.post("/upload/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def upload_documents(file: UploadFile  = File()):

     # FastAPI normally handles missing files, but this keeps the API response explicit.
     if file is None:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded.")

     file_name = file.filename 

     # Read only the file signature first so we can validate the content
     # before loading the full file into memory.
     header = await file.read(4)
     
     # Validate both the actual PDF signature and the filename extension.
     # This avoids trusting the extension alone.
     if not header.startswith(b"%PDF") or not file_name.endswith(".pdf"):
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
               detail="File signature mismatch. The file content is not a valid PDF."
          )

     # The first read moved the file pointer, so reset it before reading the full file.
     await file.seek(0)
     file_bytes = await file.read()

     try:
          # Store the document metadata/file and index its chunks into the vector store.
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
          # Always close the uploaded file handle after processing.
          await file.close()

     return {
          "success": True,
          "doc_id": indexed["doc_id"],
          "filename": indexed["filename"],
          "indexed": indexed["indexed"]
     }
     

# Return the document library metadata used by the frontend.
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Document])
async def documents():
     return list_documents()


# Return detailed metadata and a short preview for a single document.
@router.get("/{doc_id}", status_code=status.HTTP_200_OK, response_model=DocumentDetail)
async def specific_document(doc_id: str):
     try:
          document = get_doc(doc_id)

          # Read the saved PDF directly to calculate page count
          # and provide a lightweight preview without returning the full file.
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


# Delete a document from both metadata storage and the vector store.
@router.delete("/{doc_id}", status_code=status.HTTP_200_OK, response_model=dict)
async def delete_document(doc_id: str):
     try:
          remove_document(doc_id)

     except DocumentNotFoundError:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

     except Exception as e:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

     return {"success": True, "message": f"Document with id {doc_id} has been deleted."}