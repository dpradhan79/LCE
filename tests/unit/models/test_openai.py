import pytest
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from backend.ai.llm.chat_models.llm_open_ai import get_llm_chat_open_ai


@pytest.mark.llm_models
@pytest.mark.parametrize("model, reasoning",
                         [
                             (
                                     "gpt-4o-mini",
                                     {}
                             )

                         ]
                         )
def test_chat_model_ollama(model, reasoning, request):
    kwargs = {
        "temperature": 0.1, "timeout": 30}
    kwargs.update(reasoning)

    llm = get_llm_chat_open_ai(model, **kwargs)
    assert llm is not None
    messages = ChatPromptTemplate.from_messages(
        [SystemMessagePromptTemplate.from_template(template="You Are Helpful Assistant",
                                                   template_format="f-string"),
         HumanMessagePromptTemplate.from_template(template="{user_prompt}", template_format="f-string")])
    chain = messages | llm
    response = chain.invoke({
        "user_prompt": "I am Debasish, Say hello and confirm you are responding your model reference such as I am model - llama3.1:8b or gpt-oss:20b or gpt-4o-mini or any other model and let us know, if you have reasoning and tool calling capability"})
    assert (len(response.content) > 0) is True, f'Ollama Model Does Not Respond'
    print(f'\n test - {request.node.name} \n Response = \n {response.content}')
