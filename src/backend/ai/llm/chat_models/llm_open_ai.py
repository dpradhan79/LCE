import os

from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.shared.app_logger.app_logger import AppLogger
from src.shared.consts import const_config

logger = AppLogger.get_create_logger()


def get_llm_chat_open_ai(model, base_url=None, api_key: SecretStr = None,
                         **kwargs) -> ChatOpenAI | None:
    """

    :param model:
    :param base_url:
    :param api_key:
    :param kwargs:
    :return: BaseChatModel
    """

    try:
        llm = ChatOpenAI(
            model=model,
            base_url=base_url,
            api_key=api_key or SecretStr(os.getenv("OPENAI_API_KEY")),
            **kwargs  # passthrough (e.g., model_kwargs={"response_format": {"type":"json_object"}})

        )
        logger.info(f'{const_config.SYMBOLS.INFO}ChatOpenAI Initialized')
        return llm
    except Exception as e:
        logger.critical(
            f'{const_config.SYMBOLS.CRITICAL}ChatOpenAI Could Not Be Initialized, Error Type - {type(e).__name__}')
        logger.critical(f'{const_config.SYMBOLS.CRITICAL}{str(e)}')
        raise e
