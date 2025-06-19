import subprocess
import time
import subprocess
from pathlib import Path

import pytest

from core.io_client import ping


@pytest.fixture(scope="module")
def node_server():
    service_dir = Path("services/node")
    if not (service_dir / "node_modules").exists():
        subprocess.run(["npm", "install"], cwd=service_dir, check=True)
    proc = subprocess.Popen(["node", str(service_dir / "io_server.js")])
    time.sleep(1)
    yield
    proc.terminate()
    proc.wait()


def test_ping(node_server):
    assert ping("hello") == "pong:hello"
