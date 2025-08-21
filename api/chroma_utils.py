import os
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv(override=True)

PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
PERSIST_DIR = os.path.abspath(PERSIST_DIR)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")
from pydantic import SecretStr
embedding_function = OpenAIEmbeddings(model="text-embedding-3-small", api_key=SecretStr(OPENAI_API_KEY))
vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding_function)

def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.html'):
        loader = UnstructuredHTMLLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    documents = loader.load()
    return text_splitter.split_documents(documents)

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)
        for split in splits:
            split.metadata = {**split.metadata, "file_id": file_id}
        vectorstore.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_chroma(file_id: int) -> bool:
    try:
        docs = vectorstore.get(where={"file_id": file_id})
        ids = docs.get("ids", [])
        if ids:
            vectorstore.delete(ids=ids)
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {e}")
        return False