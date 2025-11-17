import streamlit as st

st.set_page_config(
    page_title="Secure Inter-Hospital Communication System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

home_page = st.Page("pages/home.py", title="Home", icon="🏠")
encrypt_page = st.Page("pages/encrypt_embed.py", title="Encrypt & Embed", icon="🔐")
decrypt_page = st.Page("pages/extract_decrypt.py", title="Extract & Decrypt", icon="🔓")
dicom_page = st.Page("pages/dicom_viewer.py", title="DICOM Viewer", icon="🩺")
analytics_page = st.Page("pages/analytics.py", title="Analytics", icon="📊")
chatbot_page = st.Page("pages/chatbot.py", title="AI Assistant", icon="🤖")

pg = st.navigation([home_page, encrypt_page, decrypt_page, dicom_page, analytics_page, chatbot_page])

pg.run()
