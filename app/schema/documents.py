from pydantic import BaseModel
from datetime import datetime
class Document(BaseModel):
     doc_id: str
     filename: str
     file_size: int
     uploaded_at: str
     
class DocumentDetail(BaseModel):
    doc_id: str
    filename: str
    file_size: int
    uploaded_at: datetime

    chunk_count: int
    indexed_status: str

    last_index_attempt: str | None
    index_error: str | None