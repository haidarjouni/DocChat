from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_ollama import ChatOllama

from .retriever import query as retriever_query
from .prompt_builder import PROMPT, format_docs

model = ChatOllama(
     model="llama2:13b"
)

retriever_query_runnable = RunnableLambda(retriever_query)
prompt_builder_runnable = RunnableLambda(format_docs)

chain = (
     {
          "context": retriever_query_runnable | prompt_builder_runnable,
          "question": RunnablePassthrough()
     }
     | PROMPT
     | model
     | StrOutputParser()
)

def ask(question):
     return chain.invoke(question)

result = ask("What protocols does the mail server use? Explain the usage of each of these protocols?")
print(result)