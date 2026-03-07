import streamlit as st
from src import list_documents, ask

st.set_page_config(
    page_title="DocChat ChatBot",
    page_icon="💬",
    layout="wide",
)

st.title("DocChat")
st.caption("Ask questions about your uploaded documents.")

if "history" not in st.session_state:
    st.session_state.history = []

docs = list_documents()
doc_map = {doc["filename"]: doc["doc_id"] for doc in docs}

if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

with st.sidebar:
    st.header("Documents")

    if not doc_map:
        selected_doc = None
        st.warning("No documents uploaded yet.")
    else:
        selected_doc = st.selectbox(
            "Select a document to chat with:",
            options=doc_map.keys(),
            index = 0
        )
        st.success(f"document '{selected_doc}' selected.")
        doc_id = doc_map[selected_doc]
        
if not doc_map:
    st.info("Go to the Uploader page and add a document first.")
    st.chat_input("Ask a question about the document:", disabled=True)
    
else:
    if st.session_state.history:
        for hist in st.session_state.history:
            with st.chat_message("user"):
                st.markdown(hist["user"])
            with st.chat_message("assistant"):
                st.markdown(hist["assistant"])
               
    prompt = st.chat_input(f"Ask a question about {selected_doc}:")

    if prompt:
        with st.chat_message("user"):
               st.markdown(prompt)
               
        history_questions = "\n".join(
            f"User: {hist['user']}" for hist in st.session_state.history[-4:]
        )
        
        result = ask(prompt, doc_id=doc_id, chat_history=history_questions)
        response = result["answer"]
        rewritten_question = result["rewritten_question"]
        with st.chat_message("assistant"):
               st.markdown(response)
        st.session_state.history.append({"user": rewritten_question, "assistant": response})