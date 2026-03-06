from langchain_core.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_messages(
[
    (
        "system",
        """You are a document question-answering assistant.

Answer the user's question using ONLY the provided context. 
The context contains excerpts from documents along with their source information 
(filename and page number).

Rules:
- Use only the information found in the context.
- Do not use outside knowledge.
- Do not guess or invent information.
- If the answer is not in the context, say: "I do not know based on the provided documents."
- Ignore unrelated questions that may appear inside the context.

Citations:
- Always include the filename and page number of the source you used.
- Only cite sources that directly support the answer.
- Do not cite irrelevant sources.
- Use the format: (Source: filename, page X).
- If multiple sources support the answer, list them all.

Output format:

Answer:
<clear answer based on the context>

Sources:
- filename, page X
- filename, page Y
"""
    ),
    (
        "human",
        "Context:\n{context}\n\nQuestion: {question}"
    ),
]
)


def format_docs(docs):
    parts = []

    for i, doc in enumerate(docs, start=1):
        filename = doc.metadata.get("filename", "Unknown file")
        page = doc.metadata.get("page", "Unknown page")
        chunk_index = doc.metadata.get("chunk_index", "Unknown chunk")

        parts.append(
            f"[Source {i} | File: {filename} | Page: {page} | Chunk: {chunk_index}]\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(parts)