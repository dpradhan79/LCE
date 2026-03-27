# pip install -qU langchain "langchain[anthropic]"
import os
from typing import List

from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.backend.ai.llm.chat_models.llm_open_ai import get_llm_chat_open_ai
from src.backend.ai.llm.llm_factory.llm_factory import SupportedLLMs
from src.shared.consts import const_config
from src.shared.utils.utils import Utility


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def multiply(a: int, b: int) -> int:
    """multiplies 2 integers - a and b and returns result."""
    return a * b


@tool()
def divide(a: int, b: int):
    """divide 2 numbers and returns result"""
    return a / b


class MathResponse(BaseModel):
    function_name: str = Field(description='function name used')
    result: int | float = Field(description=f'result returned by function - {function_name}')


class MathResponses(BaseModel):
    list_math_responses: List[MathResponse] = Field(description="list of Math Responses")


def test_agent_call_using_llm_factory():
    options = {
        "api_key": Utility.get_encrypted_key(
            os.getenv(const_config.ENV.AZURE.AZURE_OPENAI_API_KEY)),
        "base_url": os.getenv(const_config.ENV.AZURE.AZURE_OPENAI_ENDPOINT),
        "use_responses_api": True,
        # follows responses API leading multiple blocks in LLM O/P content for each type
        "reasoning": {"effort": "low", "summary": "auto"}  # reasoning not supported by gpt-4o series

    }
    llm = SupportedLLMs.get_chat_model(provider="openai", model="gpt-5.4-mini", **options)
    agent = create_agent(
        model=llm,
        tools=[get_weather, multiply, divide],
        response_format=MathResponses

        # system_prompt="You are a helpful assistant",
    )

    # Run the agent
    agent_response = agent.invoke({"messages": [("human",
                                                 """multiple 2 and 3 and divide the same to have result rounded or formatted to 2 decimal places like x.yy\n
                                                 Example - 2/3 should be rounded to 0.66, 6/3 should be rounded to 2, 7/3 should be rounded to 2.33
                                                 """)]})
    print(agent_response.get("messages")[-1].content)
    assert isinstance(agent_response.get("messages")[-1], AIMessage) is True
    assert "structured_response" in agent_response
    assert isinstance(agent_response["structured_response"], MathResponses) is True
    math_responses: MathResponses = agent_response["structured_response"]

    for ai_math_response in math_responses.list_math_responses:
        func_name = ai_math_response.function_name
        func_result = ai_math_response.result
        match func_name:
            case ("multiply"):
                assert func_result == 6
            case ("divide"):
                assert func_result == 0.67


def test_agent_call_using_get_llm_chat_open_ai():
    options = {
        "use_responses_api": True,
        # follows responses API leading multiple blocks in LLM O/P content for each type
        "reasoning": {"effort": "low", "summary": "auto"}  # reasoning not supported by gpt-4o series

    }

    llm = get_llm_chat_open_ai("gpt-5.4-mini", base_url=os.getenv(const_config.ENV.AZURE.AZURE_OPENAI_ENDPOINT),
                               api_key=Utility.get_encrypted_key(
                                   os.getenv(const_config.ENV.AZURE.AZURE_OPENAI_API_KEY)),
                               **options

                               )
    agent = create_agent(
        model=llm,
        tools=[get_weather, multiply, divide],
        response_format=MathResponses

        # system_prompt="You are a helpful assistant",
    )

    # Run the agent
    agent_response = agent.invoke({"messages": [("human",
                                                 """multiple 2 and 3 and divide the same to have result rounded or formatted to 2 decimal places like x.yy\n
                                                 Example - 2/3 should be rounded to 0.66, 6/3 should be rounded to 2, 7/3 should be rounded to 2.33
                                                 """)]})
    print(agent_response.get("messages")[-1].content)
    assert isinstance(agent_response.get("messages")[-1], AIMessage) is True
    assert "structured_response" in agent_response
    assert isinstance(agent_response["structured_response"], MathResponses) is True
    math_responses: MathResponses = agent_response["structured_response"]

    for ai_math_response in math_responses.list_math_responses:
        func_name = ai_math_response.function_name
        func_result = ai_math_response.result
        match func_name:
            case ("multiply"):
                assert func_result == 6
            case ("divide"):
                assert func_result == 0.67
