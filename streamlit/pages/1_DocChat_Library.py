import asyncio
import httpx
import streamlit as st
from services.api_client import add_document, delete_document, fetch_documents, get_specific_document 

st.set_page_config(
     page_title="DocChat Library",
     layout="wide"
)

@st.dialog("Document Viewer")
def view(doc_id: str):
    try:
        doc = asyncio.run(get_specific_document(doc_id))
    except httpx.HTTPStatusError as e:
        st.error(f"status {e.response.status_code}: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"Failed to fetch document: {e}")
        st.stop()
    st.caption(f"{doc["pages"]} page(s)")
    st.text_area(
        "Page 1 preview",
        value=doc["text"],   # preview length (adjust)
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
        try:
            result = asyncio.run(add_document(filename, file_bytes))
            st.success("Uploaded and indexed!")
            st.session_state.uploader_key += 1
            st.rerun()
        except httpx.HTTPStatusError as e:
            st.error(f"status {e.response.status_code}: {str(e)}")
        except Exception as e:
            st.error(f"Upload failed: {e}")
            
# --- Main: documents list ---
st.title("Document Library")

docs = asyncio.run(fetch_documents())
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
                            asyncio.run(delete_document(doc["doc_id"]))
                            st.success("Deleted.")
                            st.rerun()
                        except httpx.HTTPStatusError as e:
                            st.error(f"status {e.response.status_code}: {e.response.text}")
                        except Exception as e:
                            st.error(f"Failed to delete: {e}")