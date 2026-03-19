import subprocess
import time

import dotenv
import psutil
import pytest
from filelock import FileLock


@pytest.fixture(scope="session", autouse=True)
def ollama_service(tmp_path_factory, worker_id):
    dotenv.load_dotenv()
    root_tmp = tmp_path_factory.getbasetemp().parent
    lock_file = root_tmp / "ollama.lock"
    pid_file = root_tmp / "ollama.pid"
    count_file = root_tmp / "ollama.count"

    # ── BEFORE SUITE ─────────────────────────────────────
    with FileLock(str(lock_file) + ".filelock"):
        count = int(count_file.read_text()) if count_file.exists() else 0
        count_file.write_text(str(count + 1))  # ← always updated, outside if block

        if not pid_file.exists():
            print(f"\nFirst Worker Thread - [{worker_id}] Starting Ollama service...")
            process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            pid_file.write_text(str(process.pid))
            time.sleep(10)

    yield

    # ── AFTER SUITE ───────────────────────────────────────
    with FileLock(str(lock_file) + ".filelock"):
        count = int(count_file.read_text()) if count_file.exists() else 1
        remaining = count - 1
        count_file.write_text(str(remaining))  # ← decremented value written back each time

        if remaining == 0 and pid_file.exists():
            print(f"\nLast Worker Thread - [{worker_id}] — stopping Ollama...")
            pid = int(pid_file.read_text())
            try:
                # psutil works cross-platform (Windows + Linux + Mac)
                proc = psutil.Process(pid)
                proc.terminate()  # sends SIGTERM on Linux, TerminateProcess on Windows
                proc.wait(timeout=5)  # wait for clean exit
            except psutil.NoSuchProcess:
                pass  # already stopped
            except psutil.TimeoutExpired:
                proc.kill()  # force kill if it didn't stop cleanly
            finally:
                pid_file.unlink()
                count_file.unlink()
