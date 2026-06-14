import streamlit as st
import asyncio
from services.api_client import fetch_documents, send_message
st.set_page_config(
    page_title="DocChat ChatBot",
    page_icon="💬",
    layout="wide",
)

@st.dialog("Debug")
def popup(question, retrieved_chunks):
    st.write("Debugger for this question")
    st.write("**Rewritten question:**", question)

    if not retrieved_chunks:
        st.info("No retrieved chunks found.")
        return

    st.divider()
    st.write("**Retrieved chunks:**")

    for i, doc in enumerate(retrieved_chunks, start=1):
        filename = doc.get("filename", "Unknown file")
        page = doc.get("page", "Unknown page")

        with st.expander(f"Chunk {i} — {filename} — page {page}"):
            st.write(doc.get("content", "")[:500])


st.title("DocChat")
st.caption("Ask questions about your uploaded documents.")

if "history" not in st.session_state:
    st.session_state.history = []
try:
    all_docs = asyncio.run(fetch_documents())
except Exception as e:
    st.error(f"Error occurred while fetching documents: {e}")
    all_docs = []

doc_map = {doc["filename"]: doc["doc_id"] for doc in all_docs}

with st.sidebar:
    st.header("Documents")

    if not doc_map:
        selected_doc = None
        doc_id = None
        st.warning("No documents uploaded yet.")
    else:
        selected_doc = st.selectbox(
            "Select a document to chat with:",
            options=list(doc_map.keys()),
            index=0
        )
        doc_id = doc_map[selected_doc]
        st.success(f"Document '{selected_doc}' selected.")

if not doc_map:
    st.info("Go to the Uploader page and add a document first.")
    st.chat_input("Ask a question about the document:", disabled=True)

else:
    for i, hist in enumerate(st.session_state.history):
        with st.chat_message("user"):
            st.markdown(hist["user"])

        with st.chat_message("assistant"):
            st.markdown(hist["assistant"])

            if hist.get("docs"):
                if st.button("Debug", key=f"debug_{i}"):
                    popup(hist["user"], hist["docs"])

    prompt = st.chat_input(f"Ask a question about {selected_doc}:")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        history_questions = "\n".join(
            f"User: {hist['user']}" for hist in st.session_state.history[-4:]
        )
        payload = {
            "message": prompt,
            "doc_id": doc_id,
            "chat_history": history_questions
        }
        
        try:
            result = asyncio.run(send_message(payload))
        except Exception as e:
            import traceback
            st.code(traceback.format_exc())
            st.stop()
            
        response = result["answer"]
        rewritten_question = result["rewritten_question"]
        retrieved_chunks = result["docs"]

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.history.append({
            "user": rewritten_question,
            "assistant": response,
            "docs": retrieved_chunks,
        })

        st.rerun()