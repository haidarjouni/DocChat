from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
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
          "context": retriever_query_runnable | prompt_builder_runnable,
          "question": RunnableLambda(lambda x: x["question"])
     }
     | PROMPT
     | model
     | StrOutputParser()
)

def ask(user_question, doc_id=None, chat_history=None):
     rewritten_question = prompt_rewrite(user_question, chat_history)
     answer = chain.invoke({
          "question": rewritten_question,
          "doc_id": doc_id
     })
     return {
          "rewritten_question": rewritten_question,
          "answer": answer
     }