# 🎓 AI Exam & Study Assistant (Chatbot)

An intelligent **Retrieval-Augmented Generation (RAG) powered Exam & Study Assistant** that allows students to upload documents (PDF, DOCX, HTML), ask questions, and receive context-aware answers.  

The agent integrates **LangGraph, LangChain, Chroma, and Tavily Search API** to intelligently decide whether to:
- Use uploaded knowledge base (RAG)
- Perform a real-time web search
- Or directly answer with the LLM  

✅ **Frontend:** Streamlit [Live Demo](https://finalprojectatomcamp-abdulaleem.streamlit.app/)  
✅ **Backend:** FastAPI [Live API](https://final-project-atomcamp.onrender.com)  

## 📋 Table of Contents

- [Overview](#overview)
- [What Problem Does It Solve?](#what-problem-does-it-solve)
- [How It Solves These Problems](#how-it-solves-these-problems)
- [Features](#features)
  - [Core Capabilities](#core-capabilities)
  - [Technical Features](#technical-features)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)



## Overview

The AI Exam & Study Assistant is a sophisticated RAG-based application designed to revolutionize how students interact with their study materials. By leveraging advanced AI technologies, it provides intelligent responses by seamlessly combining information from uploaded documents, real-time web search, and direct AI knowledge.

## What Problem Does It Solve?

- **Information Fragmentation**: Students often struggle with scattered study materials across multiple sources
- **Context Loss**: Traditional search doesn't maintain conversation context or understand follow-up questions
- **Time-Intensive Research**: Manual searching through documents and web resources is time-consuming
- **Knowledge Gaps**: Students need access to both their specific materials and up-to-date information
- **Study Efficiency**: Difficulty in getting precise, contextual answers during study sessions

## How It Solves These Problems

- **Unified Knowledge Access**: Combines personal documents, web search, and AI knowledge in one interface
- **Intelligent Routing**: Automatically determines the best source for each query
- **Contextual Understanding**: Maintains conversation history and understands follow-up questions
- **Multi-format Support**: Handles PDF, DOCX, and HTML documents seamlessly
- **Real-time Information**: Provides current information through web search when needed

## Features

### Core Capabilities

- **🤖 Intelligent Routing**: Automatically decides between RAG, web search, and direct AI responses based on query context
- **📚 Document Management**: Upload, index, and manage study materials (PDF, DOCX, HTML)
- **🔍 Advanced RAG**: Contextual document search using Chroma vector store with query reformulation
- **🌐 Real-time Web Search**: Up-to-date information retrieval using Tavily API
- **💬 Natural Conversation**: Multi-turn conversations with persistent session memory
- **📊 Session Management**: Maintains conversation history across requests
- **🔧 Modular Architecture**: Clean, maintainable codebase with separated concerns

### Technical Features

- **Vector Search**: Advanced semantic search using OpenAI embeddings
- **Query Contextualization**: Smart reformulation of follow-up questions
- **Error Handling**: Comprehensive error management with graceful fallbacks
- **Logging**: Detailed logging for debugging and analysis
- **CORS Support**: Cross-origin resource sharing for web deployment
- **Type Safety**: Full type annotations using Pydantic models


## Tech Stack

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


### Agent Workflow

1. **Router Node**: Analyzes user queries and routes to appropriate processing path
2. **RAG Node**: Searches document knowledge base and evaluates information sufficiency
3. **Web Node**: Performs real-time web search for current information
4. **Answer Node**: Synthesizes final response using available context


## How It Works

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



## Project Structure

```
Final_Project_atomcamp/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and endpoints
│   ├── langgraph_agent.py   # LangGraph agent configuration
│   ├── nodes.py             # Agent nodes (router, RAG, web, answer)
│   ├── shared.py            # Shared state and LLM configurations
│   ├── tools.py             # RAG and web search tools
│   ├── chroma_utils.py      # Vector database operations
│   ├── langchain_utils.py   # LangChain utilities
│   ├── db_utils.py          # SQLite database operations
│   ├── utils.py             # General utility functions
│   ├── pydantic_models.py   # Data models and validation
│   └── requirements.txt     # Backend dependencies
├── frontend/
│   ├── __init__.py
│   ├── streamlit_app.py     # Main Streamlit application
│   ├── chat_interface.py    # Chat UI components
│   ├── sidebar.py           # Sidebar UI components
│   ├── api_utils.py         # API communication utilities
│   └── requirements.txt     # Frontend dependencies
├── .env                     # Environment variables
└── README.md               # This file
```


