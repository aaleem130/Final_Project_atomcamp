from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import uuid
from typing import List, Dict, Optional

def get_or_create_session_id(session_id: Optional[str]) -> str:
    return session_id or str(uuid.uuid4())

def history_to_lc_messages(history: List[Dict]) -> List[BaseMessage]:
    """Convert [{'role': 'human'|'ai', 'content': '...'}, ...] to LC messages."""
    out: List[BaseMessage] = []
    for item in history:
        role = item.get("role")
        content = item.get("content", "")
        if role == "human":
            out.append(HumanMessage(content=content))
        elif role == "ai":
            out.append(AIMessage(content=content))
    return out

def append_message(history: List[BaseMessage], message: BaseMessage) -> List[BaseMessage]:
    return history + [message]