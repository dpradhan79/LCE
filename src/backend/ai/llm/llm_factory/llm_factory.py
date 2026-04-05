from pathlib import Path
from typing import Literal, Optional

import dotenv
from langchain_core.language_models import BaseChatModel

from src.backend.ai.llm.chat_models import llm_any
from src.backend.ai.llm.chat_models.llm_ollama import _get_llm_chat_ollama
from src.backend.ai.llm.chat_models.llm_open_ai import _get_llm_chat_open_ai
from src.shared.consts.const_config import PARENT_DIR

dotenv.load_dotenv(dotenv_path=Path(PARENT_DIR))

supported_provider = Literal["ollama", "openai"]


class SupportedLLMs:
    _llm_dict = {
        "openai": _get_llm_chat_open_ai,
        "ollama": _get_llm_chat_ollama,

    }

    @classmethod
    def get_chat_model(cls,
                       model: str,
                       provider: supported_provider = Optional[str],
                       **kwargs) -> BaseChatModel:
        """
        Gets the llm instance based on provider, model
        :param provider:
        :param model:
        :param kwargs:
        :return: BaseChatModel
        """
        if provider in cls._llm_dict:
            return cls._llm_dict.get(provider)(model, **kwargs)
        else:
            return llm_any._get_llm(model_name=model, model_provider=provider, **kwargs)
