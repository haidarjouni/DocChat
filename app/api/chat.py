from fastapi import APIRouter, HTTPException, status
from app.rag.generator import ask
from app.schema.chat import MessageRequest, MessageResponse
router =  APIRouter(prefix="/api/v1/chat", tags=["documents"])

# upload and index documents
@router.post("/message/", status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def message(message: MessageRequest):
     if message.doc_id is None or message.doc_id.strip() == "":
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document ID")
     if message.message.strip() == "":
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty")
     try:
          return await ask(
               user_question=message.message,
               doc_id=message.doc_id,
               chat_history=message.chat_history
          )
     except Exception as e:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
     
     