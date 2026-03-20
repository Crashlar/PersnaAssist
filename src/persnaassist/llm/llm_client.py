import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel

# LangChain Models
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# LangGraph
from langgraph.graph import StateGraph, END

# Groq (LLaMA via OpenAI-compatible API)
from openai import OpenAI


# ==============================
# LOAD ENV
# ==============================
load_dotenv()


# ==============================
# STATE
# ==============================
class AssistantState(BaseModel):
    user_input: str
    context: str = ""
    response: Optional[str] = None
    model_used: Optional[str] = None


# ==============================
# API SETUP
# ==============================
groq_api = os.getenv("GROQ_API_KEY")
gemini_api = os.getenv("GEMINI_API_KEY")
openai_api = os.getenv("OPENAI_API_KEY")


#  Gemini (LangChain)
gemini_model = None
if gemini_api:
    gemini_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_api,
        temperature=0.7
    )


#  OpenAI (LangChain)
openai_model = None
if openai_api:
    openai_model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )


#  Groq (LLaMA)
groq_client = None
if groq_api:
    groq_client = OpenAI(
        api_key=groq_api,
        base_url="https://api.groq.com/openai/v1"
    )


# ==============================
# PROMPT BUILDER
# ==============================
def build_prompt(state):
    return f"""
    You are a helpful, intelligent voice assistant.

    Always respond clearly and naturally like a human assistant.
    Do NOT say "I couldn't process your request" unless absolutely necessary.

    Conversation history:
    {state.context}

    User: {state.user_input}

    Assistant:
    """

# ==============================
# NODE 1: LLaMA (Groq)
# ==============================
def llama_node(state: AssistantState):
    print("Trying LLaMA...")

    if not groq_client:
        print("No GROQ API key")
        return state

    try:
        res = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": build_prompt(state)}],
        )

        state.response = res.choices[0].message.content
        state.model_used = "llama"
        print("LLaMA success")

    except Exception as e:
        print("LLaMA failed:", e)

    return state


# ==============================
# NODE 2: Gemini
# ==============================
def gemini_node(state: AssistantState):
    print("Trying Gemini...")

    if not gemini_model:
        print("No Gemini model")
        return state

    try:
        res = gemini_model.invoke([
            ("system", "You are a helpful voice assistant."),
            ("human", state.user_input)
        ])

        state.response = res.content
        state.model_used = "gemini"

        print("Gemini success:", state.response)

    except Exception as e:
        print("Gemini failed:", e)

    return state


# ==============================
# NODE 3: OpenAI
# ==============================
def openai_node(state: AssistantState):
    print("Trying OpenAI...")

    if not openai_model:
        print("No OpenAI model")
        return state

    try:
        res = openai_model.invoke(build_prompt(state))

        state.response = res.content
        state.model_used = "openai"
        print("OpenAI success")

    except Exception as e:
        print("OpenAI failed:", e)

    return state


# ==============================
# ROUTERS
# ==============================
def router_after_llama(state: AssistantState):
    return END if state.response else "gemini"


def router_after_gemini(state: AssistantState):
    return END if state.response else "openai"


# ==============================
# GRAPH BUILDER
# ==============================
def build_graph():
    graph = StateGraph(AssistantState)

    graph.add_node("llama", llama_node)
    graph.add_node("gemini", gemini_node)
    graph.add_node("openai", openai_node)

    graph.set_entry_point("llama")

    graph.add_conditional_edges(
        "llama",
        router_after_llama,
        {"gemini": "gemini", END: END}
    )

    graph.add_conditional_edges(
        "gemini",
        router_after_gemini,
        {"openai": "openai", END: END}
    )

    graph.add_edge("openai", END)

    return graph.compile()


# ==============================
# MAIN CLIENT
# ==============================
class LLMClient:
    def __init__(self):
        self.graph = build_graph()

    def generate_response(self, user_input: str, context: str = "") -> str:

        state = AssistantState(
            user_input=user_input,
            context=context
        )

        result = self.graph.invoke(state)

        # LangGraph returns dict
        model_used = result.get("model_used")
        response = result.get("response")

        print(f"Model used: {model_used}")

        return response or "Sorry, I couldn't process your request."