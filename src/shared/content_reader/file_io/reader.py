from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Any, Union

from src.shared.app_logger.app_logger import AppLogger
from src.shared.consts import const_config


class Reader(ABC):
    def __init__(self, file_path: Union[str, PathLike], use_logging=True):
        self.logger = None
        if use_logging:
            self.logger = AppLogger.get_create_logger(const_config.APP_NAME)
        try:
            self.file_path = Path(file_path)
            if not self.file_path.exists():
                raise FileNotFoundError(f'File Not Found - {self.file_path}')
        except FileNotFoundError as e:
            if self.logger:
                self.logger.critical(f'File - {self.file_path} Does Not Exist')
            raise e
        except Exception as e:
            self.logger.critical(f'Exception Encountered - {type(e).__name__}')
            raise e

    @abstractmethod
    def read(self) -> Union[dict[str, Any], str]:
        raise NotImplementedError(f"Abstract method - {self.read.__qualname__} must be implemented in subclass")
