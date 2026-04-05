from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel


def _get_llm(model_name: str, **kwargs) -> BaseChatModel:
    return init_chat_model(model=model_name, **kwargs)
