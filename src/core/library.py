import json
import os
from pydoc import doc
from src.config import MANIFEST_FILE, UPLOADS_DIR
import hashlib
from datetime import datetime
def add_upload(filename, file_bytes):
     manifest = load_manifest() #load the manifest
     sha = hashlib.sha256(file_bytes).hexdigest() #create unique id using the file size
     if sha in manifest["documents"]:
          return False #check if the id already exists
     saved_name= f"{sha}_{filename}" # create a unique name using the doc_id and original filename
     save_file(saved_name=saved_name, file_bytes=file_bytes) #save the file
     manifest["documents"][sha] = {
          "filename": filename, #store the filename with the doc_id to avoid conflicts
          "file_size": len(file_bytes), #store the file size
          "path": str(UPLOADS_DIR / saved_name), #store the path to the file
          "uploaded_at": datetime.now().isoformat(), #store the upload time
          "chunk_count" : 0 #initialize chunk count to 0    
     }
     save_manifest(manifest) #save the manifest
     return True
     
def delete_doc(doc_id):
     manifest = load_manifest()
     doc = manifest["documents"].get(doc_id)
     if doc is None:
          return False #check if the doc exists     
     del manifest["documents"][doc_id] #delete the doc from manifest
     save_manifest(manifest) #save the manifest
     if os.path.exists(doc["path"]):
          os.remove(doc["path"]) #delete the file
     return True

def list_documents():
     manifest = load_manifest()
     results  = [] 
     for doc_id, doc in manifest["documents"].items(): #list of dicts with doc_id as key and doc as value
          results.append({
               "doc_id": doc_id,
               "filename": doc["filename"],
               "file_size": doc["file_size"],
               "uploaded_at": doc["uploaded_at"],
          })
     return results 

def update_doc(doc_id, updates_dict): #update a specific dict using an id
     manifest = load_manifest()
     doc = manifest["documents"].get(doc_id) #get the doc
     if doc is None:
          return False #check if empty
     doc.update(updates_dict) #update it
     save_manifest(manifest) #save changes
     return True 

def get_path(doc_id): #get the path using the doc_id
     manifest = load_manifest()
     doc = manifest["documents"].get(doc_id)
     return doc["path"] if doc else None #return the path if not exists return none

def load_manifest():
     ensure_manifest()
     if not MANIFEST_FILE.exists(): #checks if the file exists if not create it
          save_manifest({"documents": {}})
     with MANIFEST_FILE.open("r") as f:
          data = json.load(f) #read it
     return data #return data

def save_manifest(data):
     ensure_manifest()
     with MANIFEST_FILE.open("w") as f: #saves the data
          json.dump(data, f, indent=4)
        
def ensure_manifest():
     MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True) #checks if dir exists to make it 
     
def save_file(saved_name, file_bytes):
     UPLOADS_DIR.mkdir(parents=True, exist_ok=True) #checks if dir exists to make it
     with (UPLOADS_DIR / saved_name).open("wb") as f: #save the file to the uploads directory
          f.write(file_bytes) #write the file content
     return True