from typing import Literal
from langgraph.graph import StateGraph, END
from .nodes import router_node, rag_node, web_node, answer_node
from .shared import AgentState

def from_router(st: AgentState) -> Literal["rag", "answer", "end"]:
    route = st.get("route")
    if route in {"rag", "answer", "end"}:
        return route  # type: ignore
    raise ValueError(f"Invalid route: {route}")

def after_rag(st: AgentState) -> Literal["answer", "web"]:
    route = st.get("route")
    if route in {"answer", "web"}:
        return route  # type: ignore
    raise ValueError(f"Invalid route for after_rag: {route}")

g = StateGraph(AgentState)
g.add_node("router", router_node)
g.add_node("rag_lookup", rag_node)
g.add_node("web_search", web_node)
g.add_node("answer", answer_node)

g.set_entry_point("router")
g.add_conditional_edges("router", from_router, {"rag": "rag_lookup", "answer": "answer", "end": END})
g.add_conditional_edges("rag_lookup", after_rag, {"answer": "answer", "web": "web_search"})
g.add_edge("web_search", "answer")
g.add_edge("answer", END)

agent = g.compile()

