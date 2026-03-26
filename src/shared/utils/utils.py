import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import SecretStr

from src.shared.consts.const_config import LOG_FOLDER


class Utility:
    @classmethod
    def get_encrypted_key(cls, key: str) -> SecretStr:
        return SecretStr(key)

    @classmethod
    def get_secret_key(cls, key) -> SecretStr:
        return cls.get_encrypted_key(key)

    @classmethod
    def strip_markdown_fence(cls, s: str) -> str:
        s = s.strip()
        # Remove leading ```lang\n
        s = re.sub(r"^```[a-zA-Z0-9+\-]*\s*\n", "", s)
        # Remove trailing ```
        s = re.sub(r"\n```$", "", s)
        return s

    @classmethod
    def strip_wrapping_quotes(cls, s: str) -> str:
        # Remove a single pair of matching wrapping quotes if they enclose everything
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ("'", '"')):
            return s[1:-1]
        return s

    @classmethod
    def get_time_stamp(cls, zone_info: str = "Asia/Kolkata") -> str:
        time_stamp = datetime.now(ZoneInfo(zone_info)).strftime("%Y%m%d_%H%M%S")
        return time_stamp

    @classmethod
    def get_run_id(cls, zone_info: str = "Asia/Kolkata") -> str:
        time_stamp = cls.get_time_stamp(zone_info)
        return f'run_{time_stamp}'

    @classmethod
    def get_run_id_folder_path(cls, run_id: str) -> Path | None:
        run_id_folder_path = Path(os.path.join(LOG_FOLDER, run_id))
        if run_id_folder_path.exists() and run_id_folder_path.is_dir():
            shutil.rmtree(run_id_folder_path)
        run_id_folder_path.mkdir(parents=True, exist_ok=True)
        if run_id_folder_path.exists():
            return run_id_folder_path
        else:
            return None

    @classmethod
    def get_date_time_stamp(cls, folder: str) -> datetime:
        RUN_DIR_PATTERN = re.compile(r"^run_(\d{8})_(\d{6})$")
        match = RUN_DIR_PATTERN.match(folder)
        if not match:
            raise ValueError(
                f'Folder -{folder} does not follow run_id pattern in format - ("run_%Y%m%d_%H%M%S"); ex - run_20260303_120610')

        try:
            date_str, time_str = match.groups()
            dt = datetime.strptime(f'{date_str}{time_str}', '%Y%m%d%H%M%S')
            return dt
        except Exception as e:
            raise e

    @classmethod
    def find_rel_path(cls, start_path: str, end_path: str) -> Path | None:
        start = Path(start_path)
        end = Path(end_path)
        files: list = start.rglob(end.name)
        for file in files:
            if file.as_posix().endswith(end.as_posix()):
                return file
        return None
