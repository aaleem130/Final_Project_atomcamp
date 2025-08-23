# 📘 AI Exam & Study Assistant (RAG Agent)

An intelligent **Retrieval-Augmented Generation (RAG) powered Exam & Study Assistant** that allows students to upload documents (PDF, DOCX, HTML), ask questions, and receive context-aware answers.  

The agent integrates **LangGraph, LangChain, Chroma, and Tavily Search API** to intelligently decide whether to:
- Use uploaded knowledge base (RAG)
- Perform a real-time web search
- Or directly answer with the LLM  

✅ **Frontend:** Streamlit [Live Demo](https://finalprojectatomcamp-abdulaleem.streamlit.app/)  
✅ **Backend:** FastAPI [Live API](https://final-project-atomcamp.onrender.com)  

---

## ✨ Features

- **Natural Chat with Memory**: Maintains session-based conversation history across turns.  
- **Intelligent Routing**: Automatically decides whether to use:
  - RAG (documents uploaded by the user)  
  - Real-time Web Search (Tavily API)  
  - Or answer directly from the LLM  
- **RAG Integration**:  
  - Document upload (PDF, DOCX, HTML)  
  - Indexing via **Chroma Vector Store**  
  - Smart contextual query reformulation  
- **Web Search**: Real-time search using **Tavily API** when knowledge base is insufficient.  
- **Document Management**:  
  - Upload documents  
  - List all uploaded documents  
  - Delete documents  
- **Session Management**: Persistent chat history using SQLite.  
- **Comprehensive Logging**: Error and chat logs for debugging and monitoring.  
- **Modular Architecture**: Clean separation of backend services and frontend UI.  

---

## 🛠️ Tech Stack

### 🔹 Backend (FastAPI - [Repo](api/))
- **Framework**: FastAPI  
- **Knowledge Base**: Chroma Vector DB with OpenAI embeddings  
- **Search API**: Tavily API for real-time web search  
- **LLMs**: OpenAI GPT-4.1 and GPT-4.1-mini  
- **Database**: SQLite for chat history & document store  
- **Key Files**:
  - `main.py`: FastAPI app entrypoint  
  - `chroma_utils.py`: Document indexing & vector store  
  - `db_utils.py`: SQLite DB for history & documents  
  - `langchain_utils.py`: Query contextualization  
  - `langgraph_agent.py`: LangGraph agent definition  
  - `nodes.py`: Router, RAG, Web, and Answer nodes  
  - `tools.py`: Web search and RAG tools  
  - `utils.py`: Helper utilities  

### 🔹 Frontend (Streamlit - [Repo](frontend/))
- **Framework**: Streamlit  
- **Key Files**:
  - `streamlit_app.py`: Main entrypoint  
  - `chat_interface.py`: Chat UI  
  - `sidebar.py`: Document management (upload/list/delete)  
  - `api_utils.py`: Handles API calls to FastAPI backend  

---

## 🚀 How It Works

1. **Upload Documents**  
   - User uploads PDF/DOCX/HTML study material.  
   - Backend indexes and stores embeddings in **Chroma**.  

2. **Ask Questions**  
   - User asks a question via chat interface.  
   - System reformulates queries into context-aware standalone questions.  

3. **Routing Decision**  
   - If answerable directly → responds with LLM.  
   - If answer needs uploaded docs → fetches from **Chroma Vector Store**.  
   - If knowledge base lacks info → falls back to **Tavily Web Search**.  

4. **Final Answer**  
   - Combines retrieved KB and/or web snippets into a structured, accurate response.  
   - Stores Q&A in chat history for continuity.  
