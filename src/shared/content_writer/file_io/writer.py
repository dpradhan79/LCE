import logging
from abc import ABC, abstractmethod
from typing import Any

from src.shared.consts import const_config


class Writer(ABC):
    def __init__(self, use_logging: bool = True):
        self.logger = None

        if use_logging:
            self.logger = logging.getLogger(const_config.APP_NAME)

    @abstractmethod
    def write(self, data: dict[str, Any]) -> bool:
        raise NotImplementedError(f"Abstract method - {self.write.__qualname__} must be implemented in subclass")
