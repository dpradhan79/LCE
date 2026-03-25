import os

import pytest
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.backend.ai.llm.chat_models.llm_open_ai import get_llm_chat_open_ai
from src.shared.consts import const_config
from src.shared.utils.utils import Utility


@pytest.mark.llm_platform_provider_open_ai
@pytest.mark.parametrize("skip, model, options, exception_expected",
                         [
                            (False,
                              "gpt-5-chat",
                              {
                                  "use_responses_api": False,
                                  # "reasoning": {"effort": "low", "summary": "auto"} #reasoning not supported by gpt-5-chat series

                              },
                             False
                              ),

                             (False,
                              "gpt-5-chat",
                              {
                                  "use_responses_api": True,
                                  # "reasoning": {"effort": "low", "summary": "auto"} #reasoning not supported by gpt-5-chat series

                              },
                              False
                              ),
                            (False,
                              "gpt-5.4-mini",
                              {
                                  "use_responses_api": True,
                                  # follows responses API leading multiple blocks in LLM O/P content for each type
                                  "reasoning": {"effort": "low", "summary": "auto"} #reasoning not supported by gpt-4o series

                              },
                             False
                              ),
                            (False,
                              "gpt-5.4-mini",
                              {
                                  "use_responses_api": False,
                                  # follows responses API leading multiple blocks in LLM O/P content for each type
                                  "reasoning": {"effort": "low", "summary": "auto"} #reasoning not supported by gpt-4o series

                              },
                             True
                              )

                         ]
                         )
def test_chat_model_azure_open_ai(skip, model, options, exception_expected):
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
    if exception_expected:
        with pytest.raises(TypeError) as err_info:
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
            assert "Completions.create() got an unexpected keyword argument 'reasoning'" in str(err_info.value)
    else:
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


