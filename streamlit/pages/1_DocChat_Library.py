import streamlit as st
from app import add_upload, delete_doc, list_documents, get_path
from pypdf import PdfReader
from app import index_pdf
from app import chroma_delete_doc 
st.set_page_config(
     page_title="DocChat Library",
     layout="wide"
)


@st.dialog("Document Viewer")
def view(doc_id: str):
    path = get_path(doc_id)
    if not path:
        st.error("Document not found.")
        return

    with open(path, "rb") as f:
        reader = PdfReader(f)
        pages = len(reader.pages)

        st.caption(f"{pages} page(s)")
        text = reader.pages[0].extract_text() or ""

        st.text_area(
            "Page 1 preview",
            value=text[:2000],   # preview length (adjust)
            height=300,
            disabled=True,
        )
# --- Sidebar: upload only ---
with st.sidebar:
    st.title("Upload")

    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type="pdf",
        key=f"uploader_{st.session_state.uploader_key}",
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        sha = add_upload(filename, file_bytes)
        if sha:
            success = index_pdf(sha)
            if success:
                st.success("Uploaded and indexed!")
            else:
                st.error("Indexing failed")
            st.session_state.uploader_key += 1  # resets uploader
            st.rerun()
        else:
            st.warning("This file already exists.")

# --- Main: documents list ---
st.title("Document Library")

docs = list_documents()
docs = sorted(docs, key=lambda x: x["uploaded_at"], reverse=True)  # sort by upload time, newest first

if not docs:
    st.info("No documents yet. Upload a PDF from the sidebar.")
else:
    for doc in docs:
        with st.container(border=True):
            col1, col2 = st.columns([10, 1], vertical_alignment="center")

            with col1:
                    size = doc["file_size"] 
                    st.markdown(f"**{doc['filename']}**")
                    if size < 1024 * 1024:
                         size = f" {size / 1024:.2f} KB"
                    else:
                         size = f"{size / (1024 * 1024):.2f} MB"
                    st.caption(f" {size} • Uploaded:" + doc["uploaded_at"].split("T")[0])  # show file size and date, split to show only date
            with col2:
                with st.popover("⋮"):
                    st.button(
                        "View",
                        on_click=view,
                        args=(doc["doc_id"],),
                        key=f"view_{doc['doc_id']}",
                        use_container_width=True,
                    )

                    delete_clicked = st.button(
                        "Delete",
                        key=f"delete_{doc['doc_id']}",
                        type="secondary",
                        use_container_width=True,
                    )

                    if delete_clicked:
                        try:
                            chroma_delete_doc(doc["doc_id"])
                            delete_doc(doc["doc_id"])
                            st.success("Deleted.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete: {e}")
                                           
# ui is mostly by gpt-4, with some tweaks by me. I added the file size and a preview of the first page in the viewer.