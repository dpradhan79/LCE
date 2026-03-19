import os
from pathlib import Path
from typing import Literal

import dotenv
from langchain_core.language_models import BaseChatModel

from backend.ai.llm.chat_models.llm_ollama import get_llm_chat_ollama
from backend.ai.llm.chat_models.llm_open_ai import get_llm_chat_open_ai
from shared.consts.const_config import PARENT_DIR

dotenv.load_dotenv(dotenv_path=Path(PARENT_DIR))

supported_provider = Literal["ollama", "openai", "anthropic"]


class SupportedLLMs:
    llm_dict = {
        "openai": get_llm_chat_open_ai,
        "ollama": get_llm_chat_ollama,

    }

    @classmethod
    def get_chat_model(cls, provider: supported_provider = os.getenv("LLM_PROVIDER", "ollama"),
                       model: str = os.getenv("LLM_MODEL", "qwen3.5:9b"), **kwargs) -> BaseChatModel:
        """
        Gets the llm instance based on provider, model
        :param provider:
        :param model:
        :param kwargs:
        :return: BaseChatModel
        """
        return cls.llm_dict.get(provider)(model, **kwargs)
