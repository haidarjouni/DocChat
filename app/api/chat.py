from fastapi import APIRouter, HTTPException, status
from app.rag.generator import ask
from app.schema.chat import MessageRequest, MessageResponse

# Group all chat-related endpoints under a single router.
router = APIRouter(prefix="/api/v1/chat", tags=["documents"])


# Accept a user question, run it through the RAG pipeline,
# and return a grounded answer with supporting sources.
@router.post("/message/", status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def message(message: MessageRequest):

     # Retrieval requires a target document.
     if message.doc_id is None or message.doc_id.strip() == "":
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Invalid document ID"
          )

     # Prevent unnecessary LLM calls for empty messages.
     if message.message.strip() == "":
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Message cannot be empty"
          )

     try:
          return await ask(
               user_question=message.message,
               doc_id=message.doc_id,
               chat_history=message.chat_history
          )

     # Surface infrastructure/model failures as API errors.
     except HTTPException:
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Couldn't reach Ollama"
          )

     # Catch unexpected errors so the API always returns
     # a structured HTTP response instead of crashing.
     except Exception as e:
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=str(e)
          )