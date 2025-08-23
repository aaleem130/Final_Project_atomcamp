# api > main.py
from pathlib import Path
from dotenv import load_dotenv
import os
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
openai_key = os.getenv("OPENAI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

import os
import shutil
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from .db_utils import (
    insert_chat_history, get_chat_history, get_all_documents,
    insert_document_record, delete_document_record
)
from .chroma_utils import index_document_to_chroma, delete_doc_from_chroma
from .langgraph_agent import agent
from langchain_core.messages import HumanMessage, AIMessage
from .utils import get_or_create_session_id, history_to_lc_messages, append_message
from .langchain_utils import contextualise_chain

logging.basicConfig(filename='app.log', level=logging.INFO)
app = FastAPI(title="Backend - AI Exam & Study Assistant")


# CORS (allow Streamlit at :8501 and local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost:8501" 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "service": "Backend - AI Exam & Study Assistant"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    """
    Chat endpoint using LangGraph agent with routing, RAG, and web search.
    """
    session_id = get_or_create_session_id(query_input.session_id)
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model:{query_input.model.value}")

    try:
        # 1) prior messages from DB -> LangChain messages
        raw_history = get_chat_history(session_id)
        messages = history_to_lc_messages(raw_history)

        # 2) make question standalone (contextualize)
        standalone_q = contextualise_chain.invoke({
            "chat_history": messages,
            "input": query_input.question,
        })

        # 3) append current user message
        messages = append_message(messages, HumanMessage(content=standalone_q))

        # 4) run graph
        result = agent.invoke({"messages": messages, "intermediate_steps": []}) 
        
        # 5) last AI message
        last_ai = next((m for m in reversed(result["messages"]) if isinstance(m, AIMessage)), None)
        answer = last_ai.content if last_ai else "I couldn't generate a response."
        if not isinstance(answer, str):
            answer = str(answer)

        # 6) persist
        insert_chat_history(session_id, query_input.question, answer, query_input.model.value)
        logging.info(f"Session ID: {session_id}, AI Response: {answer}")
        
        # New: Get intermediate steps
        intermediate_steps = result.get("intermediate_steps", [])

        # Return a custom QueryResponse object that includes the steps
        return QueryResponse(
            answer=answer,
            session_id=session_id,
            model=query_input.model,
            intermediate_steps=intermediate_steps
        )
    except Exception as e:
        logging.exception("Chat error")
        raise HTTPException(status_code=500, detail=f"Chat error: {e}")

@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = {'.pdf', '.docx', '.html'}
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {', '.join(sorted(allowed_extensions))}")

    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = insert_document_record(file.filename)
        if file_id is None:
            raise HTTPException(status_code=500, detail="Failed to insert document record.")
        success = index_document_to_chroma(temp_file_path, file_id)

        if success:
            return {"message": f"Uploaded and indexed {file.filename}.", "file_id": file_id}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        except Exception:
            pass

@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    chroma_ok = delete_doc_from_chroma(request.file_id)
    if not chroma_ok:
        return {"error": f"Failed to delete document with file_id {request.file_id} from Chroma."}

    db_ok = delete_document_record(request.file_id)
    if db_ok:
        return {"message": f"Deleted document {request.file_id}."}
    return {"error": f"Deleted from Chroma but failed to delete document {request.file_id} from DB."}
