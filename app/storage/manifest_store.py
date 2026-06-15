import json
import os
from pydoc import doc
from app.core.config import MANIFEST_FILE, UPLOADS_DIR
import hashlib
from datetime import datetime
from app.core.exceptions import DocumentNotFoundError, DuplicateDocumentError


def add_upload(filename, file_bytes):
     manifest = load_manifest()

     # Use the file content hash as the document ID.
     # This makes duplicate detection reliable even if the filename changes.
     sha = hashlib.sha256(file_bytes).hexdigest()

     if sha in manifest["documents"]:
          raise DuplicateDocumentError()

     # Prefix the stored filename with the document ID to avoid name collisions.
     saved_name= f"{sha}_{filename}"
     save_file(saved_name=saved_name, file_bytes=file_bytes)

     # Store lightweight metadata separately from the actual PDF file.
     # Indexing fields are initialized here and updated later by the indexing pipeline.
     manifest["documents"][sha] = {
          "filename": filename,
          "file_size": len(file_bytes),
          "path": str(UPLOADS_DIR / saved_name),
          "uploaded_at": datetime.now().isoformat(),
          "chunk_count" : 0,
          "indexed_status": "never",
          "last_index_attempt": None,
          "index_error": None,
     }

     save_manifest(manifest)
     return sha
     

def delete_doc(doc_id):
     manifest = load_manifest()
     doc = manifest["documents"].get(doc_id)

     if doc is None:
          raise DocumentNotFoundError()

     # Delete the physical PDF if it still exists.
     if os.path.exists(doc["path"]):
          os.remove(doc["path"])

     # Remove the document metadata from the manifest.
     del manifest["documents"][doc_id]
     save_manifest(manifest)
     return True


def list_documents():
     manifest = load_manifest()
     results  = []

     # Return only the metadata needed by the document library UI.
     for doc_id, doc in manifest["documents"].items():
          results.append({
               "doc_id": doc_id,
               "filename": doc["filename"],
               "file_size": doc["file_size"],
               "uploaded_at": doc["uploaded_at"],
          })

     return results 


def update_doc(doc_id, updates_dict):
     manifest = load_manifest()
     doc = manifest["documents"].get(doc_id)

     if doc is None:
          return False

     # Merge partial updates into the existing document metadata.
     doc.update(updates_dict)
     save_manifest(manifest)
     return True 


def get_path(doc_id)-> str | None:
     manifest = load_manifest()
     doc = manifest["documents"].get(doc_id)
     return doc["path"] if doc else None


def load_manifest():
     ensure_manifest()

     # Create an empty manifest on first run.
     if not MANIFEST_FILE.exists():
          save_manifest({"documents": {}})

     with MANIFEST_FILE.open("r") as f:
          data = json.load(f)

     return data


def save_manifest(data):
     ensure_manifest()

     # Persist manifest changes immediately so document state survives app restarts.
     with MANIFEST_FILE.open("w") as f:
          json.dump(data, f, indent=4)
        

def ensure_manifest():
     # Ensure the data directory exists before reading or writing the manifest.
     MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
     

def save_file(saved_name, file_bytes):
     # Ensure the upload directory exists before saving PDFs.
     UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

     with (UPLOADS_DIR / saved_name).open("wb") as f:
          f.write(file_bytes)

     return True


def get_doc_name(doc_id):
     manifest = load_manifest()
     doc = manifest["documents"].get(doc_id)
     return doc["filename"] if doc else None


def get_doc(doc_id)-> dict | None:
     manifest = load_manifest()
     doc =  manifest["documents"].get(doc_id)

     if doc is None : 
          raise DocumentNotFoundError()

     # Include the document ID in the returned object because it is stored
     # as the manifest key, not inside the document metadata itself.
     return {
          "doc_id": doc_id,
          **doc
     }


def get_chunk_count(doc_id) -> int:
     manifest = load_manifest()
     doc = manifest["documents"].get(doc_id)

     # Missing documents are treated as having no indexed chunks.
     return doc["chunk_count"] if doc else 0