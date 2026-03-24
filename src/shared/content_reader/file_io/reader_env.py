import json
from os import PathLike
from pathlib import Path
from typing import Any

from typing_extensions import override

from src.shared.app_logger.app_logger import AppLogger
from src.shared.consts import const_config
from src.shared.content_reader.file_io.reader import Reader
from dotenv import dotenv_values

class EnvReader(Reader):
    def __init__(self, file_path_env: PathLike, use_logging=True):
        super().__init__(use_logging)
        self._env = Path(file_path_env)
    @override
    def read(self) -> dict[str, Any]:
        var_dict = dotenv_values(self._env)
        if self.logger:
            self.logger.debug(f'Values read from environment - {json.dumps(var_dict)}')
        return var_dict



