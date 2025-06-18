from core.memory import Memory  # noqa: E402
import pytest
from jsonschema.exceptions import ValidationError


def test_memory_load_save(tmp_path):
    path = tmp_path / "state.json"
    mem = Memory(path)
    data = {"hello": "world"}
    mem.save(data)
    assert path.exists()
    loaded = mem.load()
    assert loaded == data


def test_task_load_save_yaml(tmp_path):
    tasks = [
        {
            "id": 1,
            "description": "test",
            "component": "core",
            "dependencies": [],
            "priority": 1,
            "status": "pending",
        }
    ]
    tasks_file = tmp_path / "tasks.yml"
    mem = Memory(tmp_path / "state.json")
    mem.save_tasks(tasks, tasks_file)
    loaded = mem.load_tasks(tasks_file)
    assert loaded == tasks


def test_task_validation_error(tmp_path):
    tasks_file = tmp_path / "tasks.yml"
    tasks_file.write_text("- id: 'one'\n")
    mem = Memory(tmp_path / "state.json")
    with pytest.raises(ValidationError):
        mem.load_tasks(tasks_file)
