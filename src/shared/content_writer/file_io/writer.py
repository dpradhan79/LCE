import logging
from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Any, Union

from src.shared.consts import const_config


class Writer(ABC):
    def __init__(self, file_path: Union[str, PathLike], use_logging: bool = True):
        self.logger = None

        if use_logging:
            self.logger = logging.getLogger(const_config.APP_NAME)
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def write(self, data: dict[str, Any]) -> bool:
        raise NotImplementedError(f"Abstract method - {self.write.__qualname__} must be implemented in subclass")
