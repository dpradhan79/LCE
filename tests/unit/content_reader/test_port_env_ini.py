from pathlib import Path

import pytest

from src.shared.content_reader.file_io.env_reader import EnvReader
from src.shared.content_reader.file_io.reader import Reader
from src.shared.content_writer.file_io.writer import Writer
from src.shared.content_writer.file_io.writer_config import ConfigWriter


@pytest.mark.port
def test_port_read_env_to_ini():
    if Path(".env").exists():
        reader: Reader = EnvReader(file_path=".env", use_logging=False)
        data = reader.read()
        assert isinstance(data, dict) is True, f'Data Retrieved Is Not Dictionary Data As Expected'
        assert len(data) > 0, f'No Data Retrieved from EnvReader'

        writer: Writer = ConfigWriter('unit_test_results/env_ini.ini')
        writer.write(data)
    else:
        pytest.skip(reason=f'.env file not found')


@pytest.mark.port
def test_port_read_env_to_ini_file_not_found_exception():
    with pytest.raises(FileNotFoundError) as exc_info:
        reader: Reader = EnvReader(file_path=".env_not_found", use_logging=False)
        data = reader.read()
        assert "File Not Found" in str(exc_info)
