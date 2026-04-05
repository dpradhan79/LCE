import dotenv
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama

dotenv.load_dotenv()


def _get_llm_chat_ollama(model: str = "gpt-oss:20b", **kwargs) -> BaseChatModel:
    return ChatOllama(
        model=model,
        **kwargs
    )
