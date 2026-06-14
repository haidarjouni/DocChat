from pydantic import BaseModel

class CleanDocs(BaseModel):
     content: str
     page: int
     filename: str
     
class MessageRequest(BaseModel):
     message: str
     doc_id: str | None = None
     chat_history: str | None = None
     
class MessageResponse(BaseModel):
     answer: str
     rewritten_question: str
     docs: list[CleanDocs] | None = None
     
     
