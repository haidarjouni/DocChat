from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_OVERLAP, CHUNK_SIZE
from . import library

def index_pdf(doc_id):
     pass
     
def load_pdf(doc_id):
     doc_path = library.get_path(doc_id)
     doc_name = library.get_doc_name(doc_id) #get file name and path
     if doc_path is None:
          raise ValueError("Document not found")
     loader = PyPDFLoader(doc_path) #load the pdf using the path
     docs = loader.load() #load the pdf into a list of documents (one per page)
     for doc in docs:
          doc.metadata["doc_id"] = doc_id #foreach page/list add the doc_id to the metadata
          doc.metadata["filename"] = doc_name 
     return docs #return it

def split_chunks(docs):
     text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP) #create the splitter
     texts = [] #array to store the chunks
     texts.extend(text_splitter.split_documents(doc)) #split the documents into chunks and add them to the array
     for i, text in enumerate(texts): #foreach chunk add a unique chunk_id to the metadata using the doc_id and the chunk index
          text.metadata["chunk_id"] = f"{text.metadata['doc_id']}_chunk_{i}"
          text.metadata["chunk_index"] = i #add the chunk index to the metadata
     return texts
     
doc = load_pdf("75941c86a5333f2ed1bbd44cf4e7c0f9c6f7e4a888f841c408425b6d565ee4ae")
print(doc[0].metadata)