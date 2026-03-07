import streamlit as st
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

pg = st.navigation([
    st.Page("pages/1_DocChat_Library.py", title="Uploader page", icon="📁"),
    st.Page("pages/2_DocChat_Chat.py", title="Chat Page", icon="💬"),
    
], position="top")
pg.run()