from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Any

from src.shared.app_logger.app_logger import AppLogger
from src.shared.consts import const_config


class Reader(ABC):
    def __init__(self, use_logging:bool = True):
        self.logger = None
        if use_logging:
            self.logger = AppLogger.get_create_logger(const_config.APP_NAME)
    @abstractmethod
    def read(self) -> dict[str, Any]:
        raise NotImplementedError(f"Abstract method - {self.read.__qualname__} must be implemented in subclass")