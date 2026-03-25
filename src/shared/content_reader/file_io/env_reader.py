import json
from os import PathLike
from pathlib import Path
from typing import Any, Union

from dotenv import dotenv_values
from typing_extensions import override

from src.shared.content_reader.file_io.reader import Reader


class EnvReader(Reader):
    def __init__(self, file_path_env: Union[str, PathLike], use_logging=True):
        super().__init__(use_logging)
        try:
            self._env = Path(file_path_env)
            if not self._env.exists():
                raise FileNotFoundError(f'File Not Found - {self._env}')
        except FileNotFoundError as e:
            if self.logger:
                self.logger.critical(f'File - {self._env} Does Not Exist')
            raise e
        except Exception as e:
            self.logger.critical(f'Exception Encountered - {type(e).__name__}')
            raise e

    @override
    def read(self) -> dict[str, Any]:
        var_dict = dotenv_values(self._env)
        if self.logger:
            self.logger.debug(f'Values read from environment - {json.dumps(var_dict, indent=2)}')
        return var_dict
