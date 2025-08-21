from pydantic import SecretStr
import os
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question which might reference "
    "context in the chat history, reformulate it as a stand-alone question. "
    "Do NOT answer it. Return only the reformulated question."
)

CONTEXT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")
contextualise_chain = (
    CONTEXT_PROMPT
    | ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=SecretStr(OPENAI_API_KEY))
    | StrOutputParser()
).with_config(run_name="contextualise_chain")