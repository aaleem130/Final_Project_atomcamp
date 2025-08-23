# streamlit_app.py

import streamlit as st
from sidebar import display_sidebar
from chat_interface import display_chat_interface

st.title("AI Exam & Study Assistant")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "documents" not in st.session_state:
    st.session_state.documents = []

# Display the sidebar
display_sidebar()

# Display the chat interface
display_chat_interface()
