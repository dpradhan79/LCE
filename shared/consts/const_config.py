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
LOG_FILE = os.path.join(LOG_FOLDER, APP_NAME + '_detailed.log')
PDF_FOLDER = os.path.join(PARENT_DIR, "shared_files")


# BLOB Constants
class CONST_BLOB:
    ACCOUNT_NAME = "ACCOUNT_NAME"
    CONTAINER_NAME = "CONTAINER_NAME"
    ACCOUNT_KEY = "ACCOUNT_KEY"
    BLOB_RUN_ID = "BLOB_RUN_ID"
    RUN_FILE = "BLOB_RUN_FILE"
    USER_SCENARIO = "USER_SCENARIO"


class GRAPH_STATE_ENTRY_EXIT_NOTES:
    DELTA_SYMBOL = "\u0394"
    ENTRY_LOG = "Current Crawler Graph State (Entry State)"
    EXIT_LOG = f"Current Crawler Change ( {DELTA_SYMBOL} ) Graph State (Exit State)"
