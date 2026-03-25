import json
from os import PathLike
from typing import Any, Union

from dotenv import dotenv_values
from typing_extensions import override

from src.shared.content_reader.file_io.reader import Reader


class EnvReader(Reader):
    def __init__(self, file_path: Union[str, PathLike], use_logging=True):
        super().__init__(file_path, use_logging)

    @override
    def read(self) -> dict[str, Any]:
        var_dict = dotenv_values(self.file_path)
        if self.logger:
            self.logger.debug(f'Values read from environment - {json.dumps(var_dict, indent=2)}')
        return var_dict
