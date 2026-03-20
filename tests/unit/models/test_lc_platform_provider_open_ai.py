import os

import pytest
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from backend.ai.llm.chat_models.llm_open_ai import get_llm_chat_open_ai
from shared.consts import const_config
from shared.utils.utils import Utility


@pytest.mark.llm_models
@pytest.mark.parametrize("skip, model, options",
                         [

                             (False,
                              "gpt-5-chat",
                              {
                                  "use_responses_api": True,
                                  # follows responses API leading multiple blocks in LLM O/P content for each type
                                  # "reasoning": {"effort": "low", "summary": "auto"} #reasoning not supported by gpt-4o series

                              }
                              ),

                         ]
                         )
def test_chat_model_azure_open_ai(skip, model, options, request):
    if skip:
        pytest.skip(reason="Skipping Test As Marked")
    llm = get_llm_chat_open_ai(model, base_url=os.getenv(const_config.ENV.AZURE.AZURE_OPENAI_ENDPOINT),
                               api_key=Utility.get_encrypted_key(
                                   os.getenv(const_config.ENV.AZURE.AZURE_OPENAI_API_KEY)),
                               **options

                               )
    assert llm is not None
    messages = ChatPromptTemplate.from_messages(
        [SystemMessagePromptTemplate.from_template(template="You Are Helpful Assistant",
                                                   template_format="f-string"),
         HumanMessagePromptTemplate.from_template(template="{user_prompt}", template_format="f-string")])
    chain = messages | llm
    response = chain.invoke(
        {
            "user_prompt": """
                A farmer has 3 sons. He has 17 horses and wants to divide them as follows:
                - Eldest son gets 1/2 of the horses
                - Middle son gets 1/3 of the horses
                - Youngest son gets 1/9 of the horses
                How can this be done without killing any horse?
                Show your full reasoning step by step and finally summarize how many each son will get -.
                Format - 
                1. Eldest Son - x
                2. Middle Son - y
                3. Youngest Son - z
                where x,y,z are solutions to problem.
            """  # ← complex puzzle that FORCES reasoning
        }
    )
    assert (len(response.content) > 0) is True, f'Open AI -{model} Model Does Not Respond'
    # handles both APIs gracefully
    if isinstance(response.content, str):
        # Chat Completions API
        print(f'Response = {response.content}')

    elif isinstance(response.content, list):
        # Responses API
        for block in response.content:
            if block["type"] == "reasoning":
                for idx, s in enumerate(block.get("summary", []), start=1):
                    print(f'{idx} - Reasoning = {s.get("text")}')
            elif block["type"] == "text":
                print(f'Response = {block["text"]}')

    # get token details


def test_chat_open_ai():
    "Site - ai.azure.com/foundryProject"
    "Azure OpenAI"
    # dotenv.load_dotenv(dotenv_path=os.path.join(PARENT_DIR, ".env"))
    llm = ChatOpenAI(
        base_url="https://testauthoringagent-resource.openai.azure.com/openai/v1",
        api_key=SecretStr("6veQnGS1ZLbIeuj9KyyiQdD6Xnc0awP5Z0212MEWQKPoBSLt2okCJQQJ99CAACHYHv6XJ3w3AAAAACOGKX63"),
        model="gpt-5-chat"
        # temperature=0,
        # max_tokens=1600

    )
    messages = ChatPromptTemplate.from_messages(
        [SystemMessagePromptTemplate.from_template(template="You Are Helpful Assistant", template_format="f-string"),
         HumanMessagePromptTemplate.from_template(template="{user_prompt}", template_format="f-string")])
    chain = messages | llm
    response = chain.invoke({
        "user_prompt": """
                A farmer has 3 sons. He has 17 horses and wants to divide them as follows:
                - Eldest son gets 1/2 of the horses
                - Middle son gets 1/3 of the horses
                - Youngest son gets 1/9 of the horses
                How can this be done without killing any horse?
                Show your full reasoning step by step and finally summarize how many each son will get -.
                Format - 
                1. Eldest Son - x
                2. Middle Son - y
                3. Youngest Son - z
                where x,y,z are solutions to problem.
            """  # ← complex puzzle that FORCES reasoning
    }
    )
    assert response.content is not None
    assert (len(response.content) > 0) is True
    print(response.content)
