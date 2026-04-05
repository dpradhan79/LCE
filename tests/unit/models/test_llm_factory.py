import pytest
from langchain_core.language_models import BaseChatModel

from src.backend.ai.llm.llm_factory.llm_factory import SupportedLLMs


@pytest.mark.llm_factory
def test_llm_factory_any():
    kwargs = {"reasoning": True, "temperature": 0.1, "timeout": 30}
    ollama_val = SupportedLLMs._llm_dict.pop("ollama")
    llm: BaseChatModel = None
    try:
        llm = SupportedLLMs.get_chat_model(provider="ollama", model="gpt-oss:20b", **kwargs)

    except Exception as e:
        pytest.fail(f"Failed to get ollama model from factory with error {e}")
    finally:
        if "ollama" not in SupportedLLMs._llm_dict:
            SupportedLLMs._llm_dict["ollama"] = ollama_val
    assert type(llm).__name__ == "ChatOllama", "Ollama Model Was Not Retrieved"


@pytest.mark.llm_factory
def test_llm_factory_open_ai():
    kwargs = {
        "use_responses_api": True,
        "reasoning": {"effort": "low", "summary": "auto"}
    }

    llm: BaseChatModel = None
    try:
        llm = SupportedLLMs.get_chat_model(model="gpt-5.4-nano", provider="openai", **kwargs)

    except Exception as e:
        pytest.fail(f"Failed to get ollama model from factory with error {e}")

    assert type(llm).__name__ == "ChatOpenAI", "Ollama Model Was Not Retrieved"
