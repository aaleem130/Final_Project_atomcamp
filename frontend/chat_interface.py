# chat_interface.py

import streamlit as st
from api_utils import get_api_response

def display_chat_interface():
    # Display chat messages from session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user query
    if prompt := st.chat_input("Query:"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant's response
        with st.spinner("Generating response..."):
            model = st.session_state.get("model", "gpt-4.1-mini")
            response = get_api_response(prompt, st.session_state.session_id, model)
            
            if response:
                st.session_state.session_id = response.get('session_id')
                assistant_message = response.get('answer', 'No answer provided.')
                
                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                with st.chat_message("assistant"):
                    st.markdown(assistant_message)
                    
                    # Display response details
                    with st.expander("Response Details"):
                        st.json(response)
            else:
                st.error("Failed to get a response from the API. Please try again.")