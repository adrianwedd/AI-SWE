import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

@pytest.fixture(scope="session", autouse=True)
def add_project_root_to_sys_path():
    yield
    if str(ROOT) in sys.path:
        sys.path.remove(str(ROOT))
