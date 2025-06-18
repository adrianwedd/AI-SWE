import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.memory import Memory


def test_memory_load_save(tmp_path):
    path = tmp_path / "state.json"
    mem = Memory(path)
    data = {"hello": "world"}
    mem.save(data)
    assert path.exists()
    loaded = mem.load()
    assert loaded == data
