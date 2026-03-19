import os

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def get_llm_chat_open_ai(model, **kwargs) -> BaseChatModel:
    "Site - ai.azure.com/foundryProject"
    "Chat OpenAI"

    llm = ChatOpenAI(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        **kwargs,  # passthrough (e.g., model_kwargs={"response_format": {"type":"json_object"}})

    )
    return llm
