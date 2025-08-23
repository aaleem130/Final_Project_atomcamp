# sidebar.py

import streamlit as st
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # Sidebar: Model Selection
    model_options = ["gpt-4.1-mini", "gpt-4.1"]  
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # --- Document Management ---
    st.sidebar.header("Document Management")
    
    # Upload Document Section
    with st.sidebar.expander("Upload New Document", expanded=True):
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "html"], label_visibility="collapsed")
        if uploaded_file:
            if st.button("Upload Document"):
                with st.spinner("Uploading..."):
                    upload_response = upload_document(uploaded_file)
                    if upload_response and upload_response.get('file_id'):
                        st.session_state.documents = list_documents()  # Refresh the list
                        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                    else:
                        st.error("Failed to upload file.")

    # List & Delete Documents Section
    with st.sidebar.expander("Manage Uploaded Documents", expanded=True):
        if st.button("Refresh Document List"):
            with st.spinner("Refreshing..."):
                st.session_state.documents = list_documents()
                st.success("Document list refreshed!")
        
        documents = st.session_state.documents
        if documents:
            st.write("---")
            for doc in documents:
                col1, col2 = st.columns([0.7, 0.3])
                col1.text(f"{doc['filename']} (ID: {doc['id']})")
                if col2.button("Delete", key=f"del_{doc['id']}"):
                    with st.spinner("Deleting..."):
                        delete_response = delete_document(doc['id'])
                        if delete_response:
                            st.session_state.documents = list_documents()  # Refresh the list
                            st.success(f"Document with ID {doc['id']} deleted.")
                        else:
                            st.error(f"Failed to delete document with ID {doc['id']}.")
                            
        else:
            st.info("No documents uploaded yet.")
