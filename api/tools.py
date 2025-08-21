import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from .chroma_utils import vectorstore

load_dotenv(override=True)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not set in environment variables.")

tavily = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=3,
    topic="general"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

@tool
def web_search_tool(query: str) -> str:
    """Up-to-date web info via Tavily."""
    try:
        result = tavily.invoke({"query": query})
        results = result.get("results", []) if isinstance(result, dict) else result
        parts = []
        for item in results:
            title = item.get("title", "No title")
            content = item.get("content", "No content")
            url = item.get("url", "")
            parts.append(f"**{title}**\n{content}\n🔗 {url}")
        return "\n\n".join(parts) if parts else "No results found."
    except Exception as e:
        return f"WEB_ERROR::{e}"

@tool
def rag_search_tool(query: str) -> str:
    """Top-3 chunks from KB (empty string if none)."""
    try:
        docs = retriever.invoke(query)
        return "\n\n".join(d.page_content for d in docs) if docs else ""
    except Exception as e:
        return f"RAG_ERROR::{e}"