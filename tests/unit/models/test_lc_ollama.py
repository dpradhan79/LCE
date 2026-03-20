import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from backend.ai.llm.chat_models.llm_ollama import get_llm_chat_ollama


async def invoke_llm_with_timeout(llm: BaseChatModel, message, timeout: int = 30):
    import asyncio
    try:

        return await asyncio.wait_for(llm.ainvoke(message), timeout=timeout)
    except asyncio.TimeoutError as e:
        raise TimeoutError from e


@pytest.mark.llm_models
@pytest.mark.parametrize("model, reasoning",
                         [
                             ("gpt-oss:20b", True),
                             ("qwen2.5-coder:7b", False),
                             ("qwen3.5:9b", True)
                         ]
                         )
def test_chat_model_ollama(model, reasoning, request):
    kwargs = {"reasoning": reasoning, "temperature": 0.1, "timeout": 30}
    if model != "qwen3.5:0.8b":
        llm = get_llm_chat_ollama(model, **kwargs)
        assert llm is not None
        messages = ChatPromptTemplate.from_messages(
            [SystemMessagePromptTemplate.from_template(template="You Are Helpful Assistant",
                                                       template_format="f-string"),
             HumanMessagePromptTemplate.from_template(template="{user_prompt}", template_format="f-string")])
        chain = messages | llm
        response = chain.invoke({
            "user_prompt": "I am Debasish, Say hello and confirm you are responding your model reference such as I am model - llama3.1:8b or gpt-oss:20b or any other model"})
        assert (len(response.content) > 0) is True, f'Ollama Model - {model} Does Not Respond'
        print(f'\n test - {request.node.name} \n Response = \n {response.content}')
    elif model == "qwen3.5:0.8b":
        llm = get_llm_chat_ollama(model, **kwargs)
        messages = ChatPromptTemplate.from_messages(
            [SystemMessagePromptTemplate.from_template(template="You Are Helpful Assistant",
                                                       template_format="f-string"),
             HumanMessagePromptTemplate.from_template(template="{user_prompt}",
                                                      template_format="f-string")]).format_messages(
            user_prompt="I am Debasish, Say hello and confirm you are responding your model reference such as I am model - llama3.1:8b or gpt-oss:20b or any other model")
        import asyncio
        response = asyncio.run(invoke_llm_with_timeout(llm, messages))
        assert (len(response.content) > 0) is True, f'Ollama Model Does Not Respond'
        print(f'\n test - {request.node.name} \n Response = \n {response.content}')
