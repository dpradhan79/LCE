"""
constant default model for the application
"""
import os
from pathlib import Path

# other constants can be added here as needed
# get the parent folder of the project

file_sep_char = os.sep

PARENT_DIR = Path(__file__).parents[2]
APP_NAME = PARENT_DIR.stem
LOG_FOLDER = os.path.join(PARENT_DIR, 'Logs')
LOG_FILE = APP_NAME + '_detailed.log'
PDF_FOLDER = os.path.join(PARENT_DIR, "shared_files")


# BLOB Constants
class CONST_BLOB:
    ACCOUNT_NAME = "ACCOUNT_NAME"
    CONTAINER_NAME = "CONTAINER_NAME"
    ACCOUNT_KEY = "ACCOUNT_KEY"
    BLOB_RUN_ID = "BLOB_RUN_ID"
    RUN_FILE = "BLOB_RUN_FILE"
    USER_SCENARIO = "USER_SCENARIO"


class ENV:
    class LLM:
        LLM_PROVIDER = "LLM_PROVIDER"
        LLM_MODEL = "LLM_MODEL"

    class OPEN_AI:
        OPENAI_API_KEY = "OPENAI_API_KEY"

    class AZURE:
        AZURE_OPENAI_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
        AZURE_OPENAI_API_VERSION = "AZURE_OPENAI_API_VERSION"
        AZURE_LLM_MODEL = "AZURE_LLM_MODEL"
        AZURE_OPENAI_API_KEY = "AZURE_OPENAI_API_KEY"


class GRAPH_STATE_ENTRY_EXIT_NOTES:
    DELTA_SYMBOL = "\u0394"
    ENTRY_LOG = "Current Crawler Graph State (Entry State)"
    EXIT_LOG = f"Current Crawler Change ( {DELTA_SYMBOL} ) Graph State (Exit State)"
