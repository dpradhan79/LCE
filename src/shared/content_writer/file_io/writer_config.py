import json
from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from typing import Any

from typing_extensions import override

from src.shared.content_writer.file_io.writer import Writer


class ConfigIniFile(Writer):
    def __init__(self, file_path: PathLike, use_logging:bool = True):
        super().__init__(use_logging)
        self._ini_file = Path(file_path)

    @override
    def write(self, data: dict[str, Any]):
        config = ConfigParser()
        for section, kv in data.items():
            config[section] = {}
            for k,v in kv.items():
                config[section][k]=v
        with open(self._ini_file, "w") as f:
            config.write(f)
        if self.logger:
            self.logger.debug(f'Config File Updated With Data - {json.dumps(data)}')





