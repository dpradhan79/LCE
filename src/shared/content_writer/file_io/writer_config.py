import json
from configparser import ConfigParser
from os import PathLike
from typing import Any, Union

from typing_extensions import override

from src.shared.content_writer.file_io.writer import Writer


class ConfigWriter(Writer):
    def __init__(self, file_path: Union[str, PathLike], use_logging: bool = True):
        super().__init__(file_path, use_logging)

    @override
    def write(self, data: dict[str, Any]):
        try:
            config = ConfigParser()
            is_flat = all(not isinstance(v, dict) for v in data.values())
            if is_flat:
                data = {"DEFAULT": data}
            for section, kv in data.items():
                config[section] = {}
                for k, v in kv.items():
                    config[section][k] = v
            with open(self.file_path, "w") as f:

                config.write(f)
            if self.logger:
                self.logger.debug(f'Config File - {self.file_path} Updated With Data - {json.dumps(data)}')
        except Exception as e:
            if self.logger:
                self.logger.critical(f'Exception encountered - {type(e).__name__}')
            raise e
        write_status = True
        return write_status
