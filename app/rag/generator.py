from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama

from .retriever import retriever_query
from .prompt_builder import PROMPT, format_docs
from .rewriter import prompt_rewrite 
model = ChatOllama(
     model="llama2:13b"
)

retriever_query_runnable = RunnableLambda(retriever_query)
prompt_builder_runnable = RunnableLambda(format_docs)

chain = (
     {
          "context":  RunnableLambda(lambda x: x["context"]),
          "question": RunnableLambda(lambda x: x["question"])
     }
     | PROMPT
     | model
     | StrOutputParser()
)

def ask(user_question, doc_id=None, chat_history=None):
     rewritten_question = prompt_rewrite(user_question, chat_history)
     docs = retriever_query({
          "question": rewritten_question,
          "doc_id": doc_id
     })
     
     context = format_docs(docs)
     
     answer = chain.invoke({
          "context": context,
          "question": rewritten_question    
     })
 
     return {
          "rewritten_question": rewritten_question,
          "answer": answer,
          "docs": serialize_docs(docs),        
     }
     
def serialize_docs(documents) -> list[dict]:
     return [
          {
               "content": doc.page_content,
               "page": doc.metadata.get("page", "Unkown"),
               "filename": doc.metadata.get("filename", "Unkown") # metadata is dict that how u work with dict
          } for doc in documents
     ]