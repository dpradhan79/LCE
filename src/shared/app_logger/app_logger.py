import logging
import sys
from logging import Logger
from typing import Dict, Literal

from src.shared.consts import const_config
from src.shared.consts.const_config import LOG_FILE, SYMBOLS
from src.shared.utils.utils import Utility


class SymbolLogger(logging.Logger):
    """
    Custom Logger that automatically prepends the appropriate symbol
    to every log message based on its level.

    Eliminates the need to manually write:
        logger.info(f'{SYMBOLS.INFO} some message')

    Instead, just write:
        logger.info('some message')

    and the symbol is injected automatically.
    """

    def debug(self, msg, *args, **kwargs):
        kwargs.setdefault('stacklevel', 2)
        super().debug(f'{SYMBOLS.DEBUG} {msg}', *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        kwargs.setdefault('stacklevel', 2)
        super().info(f'{SYMBOLS.INFO} {msg}', *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        kwargs.setdefault('stacklevel', 2)
        super().warning(f'{SYMBOLS.WARN} {msg}', *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        kwargs.setdefault('stacklevel', 2)
        super().error(f'{SYMBOLS.ERROR} {msg}', *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        kwargs.setdefault('stacklevel', 2)
        super().critical(f'{SYMBOLS.CRITICAL} {msg}', *args, **kwargs)


class AppLogger:
    _dict_logger: Dict[str, Logger] = {}
    LOG_LEVEL = Literal["Debug", "Info", "Warning", "Error", "Critical"]
    _dict_log_level = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    @classmethod
    def get_create_logger(cls, app_name: str = const_config.APP_NAME, log_level: LOG_LEVEL = "Info",
                          first_call=False) -> Logger:
        if app_name in cls._dict_logger and first_call is False:
            return cls._dict_logger[app_name]
        log_run_folder = Utility.get_run_id_folder_path(run_id=Utility.get_run_id())
        logger = logging.getLogger(app_name)
        for handler in logger.handlers:
            handler.close()
        logger.handlers.clear()
        logger.setLevel(cls._dict_log_level[log_level.lower()])
        if not logger.handlers:
            # file handlder

            fh = logging.FileHandler(log_run_folder / LOG_FILE, mode="w", encoding="utf-8")

            fmt = logging.Formatter(
                "%(asctime)s %(levelname)s "
                "[%(name)s %(filename)s:%(lineno)d %(funcName)s] %(message)s"
            )
            fh.setFormatter(fmt)
            fh.setLevel(logging.DEBUG)

            # stream handler for console output

            console = logging.StreamHandler(stream=sys.stdout)
            fmt = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="%H:%M:%S")
            console.setFormatter(fmt)
            console.setLevel(logging.INFO)

            # add handler to logger
            logger.addHandler(fh)
            logger.addHandler(console)
            logger.propagate = False
        cls._dict_logger[app_name] = logger
        logger.info(f'{const_config.SYMBOLS.INFO} Log Initialized @- {log_run_folder / LOG_FILE}')
        return logger
