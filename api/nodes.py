
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from .shared import AgentState, router_llm, judge_llm, answer_llm, RouteDecision, RagJudge
from .tools import rag_search_tool, web_search_tool

def router_node(state: AgentState) -> AgentState:
    """Route the user query to RAG, web, answer, or end."""
    system_prompt = (
        "You are a router:\n"
        "- 'end' for greetings/small-talk (also include a reply)\n"
        "- 'rag' when KB lookup is needed\n"
        "- 'answer' when you can answer directly"
    )
    messages = [SystemMessage(content=system_prompt)] + state.get("messages", [])
    try:
        result = router_llm.invoke(messages)
        if isinstance(result, dict):
            result = RouteDecision(**result)
        route = getattr(result, "route", None)
        reply = getattr(result, "reply", None) or "Hello!"
    except Exception as e:
        route = "end"
        reply = f"ROUTER_ERROR::{e}"
    route = route or "end"
    out: AgentState = {"messages": state.get("messages", []), "route": route}
    if route == "end":
        out["messages"] = state.get("messages", []) + [AIMessage(content=reply)]
    return out

def rag_node(state: AgentState) -> AgentState:
    """Retrieve KB chunks and judge sufficiency."""
    query = next(
        (m.content for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)),
        ""
    )
    try:
        chunks = rag_search_tool.invoke({"query": query})
        judge_messages = [
            ("system", "Judge whether the retrieved information is sufficient."),
            ("user", f"Question: {query}\n\nRetrieved:\n{chunks}\n\nIs this sufficient?")
        ]
        verdict = judge_llm.invoke(judge_messages)
        if isinstance(verdict, dict):
            verdict = RagJudge(**verdict)
        sufficient = getattr(verdict, "sufficient", False)
        route = "answer" if sufficient else "web"
    except Exception as e:
        chunks = f"RAG_ERROR::{e}"
        route = "web"
    out: AgentState = {**state, "rag": chunks, "route": route, "messages": state.get("messages", [])}
    return out

def web_node(state: AgentState) -> AgentState:
    """Retrieve web snippets and set route to answer."""
    query = next(
        (m.content for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)),
        ""
    )
    try:
        snippets = web_search_tool.invoke({"query": query})
    except Exception as e:
        snippets = f"WEB_ERROR::{e}"
    out: AgentState = {**state, "web": snippets, "route": "answer", "messages": state.get("messages", [])}
    return out

def answer_node(state: AgentState) -> AgentState:
    """Generate final answer using KB and/or web context."""
    user_q = next(
        (m.content for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)),
        ""
    )
    ctx_parts = []
    if state.get("rag"):
        ctx_parts.append("Knowledge Base Information:\n" + str(state.get("rag")))
    if state.get("web"):
        ctx_parts.append("Web Search Results:\n" + str(state.get("web")))
    context = "\n\n".join(ctx_parts) if ctx_parts else "No external context available."
    prompt = (
        f"Answer the user's question using the context.\n\n"
        f"Question: {user_q}\n\nContext:\n{context}\n\n"
        f"Provide a helpful, accurate, concise response."
    )
    messages = state.get("messages", []) + [HumanMessage(content=prompt)]
    try:
        result = answer_llm.invoke(messages)
        ans = getattr(result, "content", None)
    except Exception as e:
        ans = f"ANSWER_ERROR::{e}"
    out: AgentState = {
        **state,
        "messages": state.get("messages", []) + [
            AIMessage(content=ans if ans is not None else str(ans))
        ]
    }
    return out

