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

















# AI Exam & Study Assistant 🎓

An intelligent RAG (Retrieval-Augmented Generation) powered study companion that helps students learn more effectively by combining document knowledge, web search, and AI reasoning capabilities.

## 🌟 Live Demo

- **Frontend (Streamlit)**: [https://finalprojectatomcamp-abdulaleem.streamlit.app/](https://finalprojectatomcamp-abdulaleem.streamlit.app/)
- **Backend API**: [https://final-project-atomcamp.onrender.com](https://final-project-atomcamp.onrender.com)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

The AI Exam & Study Assistant is a sophisticated RAG-based application designed to revolutionize how students interact with their study materials. By leveraging advanced AI technologies, it provides intelligent responses by seamlessly combining information from uploaded documents, real-time web search, and direct AI knowledge.

### What Problem Does It Solve?

- **Information Fragmentation**: Students often struggle with scattered study materials across multiple sources
- **Context Loss**: Traditional search doesn't maintain conversation context or understand follow-up questions
- **Time-Intensive Research**: Manual searching through documents and web resources is time-consuming
- **Knowledge Gaps**: Students need access to both their specific materials and up-to-date information
- **Study Efficiency**: Difficulty in getting precise, contextual answers during study sessions

### How It Solves These Problems

- **Unified Knowledge Access**: Combines personal documents, web search, and AI knowledge in one interface
- **Intelligent Routing**: Automatically determines the best source for each query
- **Contextual Understanding**: Maintains conversation history and understands follow-up questions
- **Multi-format Support**: Handles PDF, DOCX, and HTML documents seamlessly
- **Real-time Information**: Provides current information through web search when needed

## ✨ Features

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

## 🏗️ Architecture

The application follows a modern microservices architecture with clear separation between frontend and backend:

```
┌─────────────────┐    HTTP/REST    ┌──────────────────┐
│   Streamlit     │ ◄──────────────► │   FastAPI        │
│   Frontend      │                  │   Backend        │
└─────────────────┘                  └──────────────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │   LangGraph      │
                                     │   Agent          │
                                     └──────────────────┘
                                              │
                        ┌─────────────────────┼─────────────────────┐
                        ▼                     ▼                     ▼
                ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
                │   Router     │    │   RAG Node   │    │   Web Node   │
                │   Node       │    │              │    │              │
                └──────────────┘    └──────────────┘    └──────────────┘
                                            │                     │
                                            ▼                     ▼
                                    ┌──────────────┐    ┌──────────────┐
                                    │   Chroma     │    │   Tavily     │
                                    │   Vector DB  │    │   Search API │
                                    └──────────────┘    └──────────────┘
```

### Agent Workflow

1. **Router Node**: Analyzes user queries and routes to appropriate processing path
2. **RAG Node**: Searches document knowledge base and evaluates information sufficiency
3. **Web Node**: Performs real-time web search for current information
4. **Answer Node**: Synthesizes final response using available context

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance web framework for building APIs
- **LangChain**: Framework for developing LLM applications
- **LangGraph**: Library for building stateful, multi-actor applications with LLMs
- **OpenAI GPT**: Language models for text generation and embeddings
- **ChromaDB**: Vector database for document storage and retrieval
- **Tavily**: Search API for real-time web information
- **SQLite**: Lightweight database for session and document management
- **Pydantic**: Data validation and settings management

### Frontend
- **Streamlit**: Framework for building interactive web applications
- **Requests**: HTTP library for API communication

### Infrastructure
- **Render**: Backend deployment and hosting
- **Streamlit Cloud**: Frontend deployment and hosting

## 🚀 Installation

### Prerequisites

- Python 3.8+
- OpenAI API Key
- Tavily API Key

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-exam-study-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install backend dependencies**
```bash
cd api
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

5. **Run the backend**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install frontend dependencies**
```bash
cd frontend
pip install -r requirements.txt
```

2. **Update backend URL**
In `frontend/api_utils.py`, update the `BACKEND_URL` to point to your backend:
```python
BACKEND_URL = "http://localhost:8000"  # For local development
```

3. **Run the frontend**
```bash
streamlit run streamlit_app.py
```

## 📖 Usage

### Getting Started

1. **Access the Application**: Open the Streamlit frontend in your browser
2. **Upload Documents**: Use the sidebar to upload your study materials (PDF, DOCX, HTML)
3. **Start Chatting**: Ask questions about your documents or any topic
4. **Manage Documents**: View, refresh, or delete uploaded documents as needed

### Example Interactions

**Document-based Query:**
```
User: "What are the main concepts in the uploaded physics textbook?"
Assistant: [Searches through uploaded documents and provides relevant information]
```

**Web Search Query:**
```
User: "What are the latest developments in quantum computing?"
Assistant: [Performs web search and provides current information]
```

**Follow-up Question:**
```
User: "Can you explain that in simpler terms?"
Assistant: [Understands context and provides simplified explanation]
```

### Model Selection

Choose between available OpenAI models:
- **GPT-4.1-Mini**: Faster, cost-effective for most queries
- **GPT-4.1**: More capable for complex reasoning tasks

## 📚 API Documentation

### Core Endpoints

#### Chat Endpoint
```http
POST /chat
```

**Request Body:**
```json
{
    "question": "Your question here",
    "session_id": "optional_session_id",
    "model": "gpt-4.1-mini"
}
```

**Response:**
```json
{
    "answer": "AI generated response",
    "session_id": "session_identifier",
    "model": "gpt-4.1-mini",
    "intermediate_steps": []
}
```

#### Document Upload
```http
POST /upload-doc
```

**Request:** Multipart form data with file
**Response:**
```json
{
    "message": "Uploaded and indexed filename.pdf",
    "file_id": 123
}
```

#### List Documents
```http
GET /list-docs
```

**Response:**
```json
[
    {
        "id": 1,
        "filename": "document.pdf",
        "upload_timestamp": "2025-01-15T10:30:00"
    }
]
```

#### Delete Document
```http
POST /delete-doc
```

**Request Body:**
```json
{
    "file_id": 123
}
```

## 📁 Project Structure

```
ai-exam-study-assistant/
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

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models and embeddings | Yes |
| `TAVILY_API_KEY` | Tavily API key for web search | Yes |

### Model Configuration

The application supports multiple OpenAI models:
- **gpt-4.1-mini**: Default model for most operations
- **gpt-4.1**: Available for complex reasoning tasks

### Vector Store Configuration

- **Embedding Model**: `text-embedding-3-small`
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Top K Results**: 3 documents

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests if applicable**
5. **Commit your changes**
   ```bash
   git commit -m "Add your feature description"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for public methods
- Write tests for new functionality
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. **Check the Issues**: Look for existing issues on GitHub
2. **Create New Issue**: If your problem isn't covered, create a new issue
3. **Provide Details**: Include error messages, steps to reproduce, and system information

## 🔮 Future Enhancements

- [ ] Support for additional document formats (PPTX, TXT, CSV)
- [ ] Advanced document summarization features
- [ ] Multi-language support
- [ ] User authentication and personalized knowledge bases
- [ ] Integration with popular study platforms
- [ ] Mobile application development
- [ ] Advanced analytics and study progress tracking

## 🙏 Acknowledgments

- **OpenAI** for providing powerful language models
- **LangChain** team for the excellent framework
- **Streamlit** for the intuitive frontend framework
- **Tavily** for reliable web search capabilities
- **ChromaDB** for efficient vector storage

---

**Built with ❤️ for students worldwide**

*Star ⭐ this repository if you find it helpful!*
