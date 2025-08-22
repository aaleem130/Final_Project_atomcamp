# api_utils.py

import requests
import streamlit as st
from typing import Optional, List, Dict, Any

BACKEND_URL = "https://final-project-atomcamp.onrender.com"

def get_api_response(question: str, session_id: Optional[str], model: str) -> Optional[Dict[str, Any]]:
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "question": question,
        "model": model,
        "session_id": session_id
    }

    try:
        response = requests.post(f"{BACKEND_URL}/chat", headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

def upload_document(file) -> Optional[Dict[str, Any]]:
    print("Uploading file...")
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{BACKEND_URL}/upload-doc", files=files, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while uploading the file: {e}")
        return None

def list_documents() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BACKEND_URL}/list-docs", timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the document list: {e}")
        return []

def delete_document(file_id: int) -> Optional[Dict[str, Any]]:
    headers = {
        'Content-Type': 'application/json'
    }
    data = {"file_id": file_id}

    try:
        response = requests.post(f"{BACKEND_URL}/delete-doc", headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while deleting the document: {e}")
        return None
