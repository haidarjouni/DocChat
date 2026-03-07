from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

model = ChatOllama(
     model="llama3.2:3b"
)

prompt = ChatPromptTemplate.from_messages([
     (
          "system",
          """
               You rewrite follow-up user questions into standalone questions for document retrieval.

               Rules:
               - Return only ONE rewritten question.
               - Do not answer the question.
               - Do not explain anything.
               - Do not add labels like "Rewritten question".
               - If the question is already standalone, return it unchanged.
               - Use the history only to resolve references like "it", "they", "this", or "that".
          """
     ),

    # ---- FEW SHOT EXAMPLES ----

    (
        "human",
          """
               History:
               User: What is DNS?
               User: What is DNS caching?

               New question:
               Why is it useful?
          """
    ),
    (
        "ai",
        "Why is DNS caching useful?"
    ),

    (
          "human",
          """
               History:
               User: What protocols does a mail server use?
               User: What is POP3?

               New question:
               How does it retrieve emails?
          """
     ),
     (
          "ai",
          "How does POP3 retrieve emails?"
     ),

    (
          "human",
          """
               History:
               User: What is ARP?
               User: How does ARP find MAC addresses?

               New question:
               Why is it important?
          """
          ),
     (
          "ai",
          "Why is ARP important?"
     ),

    # ---- REAL INPUT ----

     (
        "human",
        """History:
          {history}

          New question:
          {question}"""
     )
])

chain = (
     prompt
     | model
     | StrOutputParser()
)

def prompt_rewrite(question, chat_history):
    if not chat_history.strip():
        return question

    result = chain.invoke({
        "history": chat_history,
        "question": question
    }).strip()

    first_line = result.splitlines()[0].strip()

    prefixes = [
        "rewritten question:",
        "standalone question:",
        "question:",
    ]

    lowered = first_line.lower()
    for prefix in prefixes:
        if lowered.startswith(prefix):
            first_line = first_line[len(prefix):].strip()
            break

    return first_line