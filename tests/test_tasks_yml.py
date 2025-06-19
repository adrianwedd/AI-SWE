import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_tasks_file_starts_with_schema_comment():
    tasks_file = ROOT / "tasks.yml"
    with tasks_file.open() as f:
        first_line = f.readline().strip()
    assert first_line.startswith("# jsonschema:"), "tasks.yml must start with jsonschema comment block"

def test_task_ids_unique():
    tasks_file = ROOT / "tasks.yml"
    with tasks_file.open() as f:
        tasks = yaml.safe_load(f)
    ids = [task["id"] for task in tasks]
    assert len(ids) == len(set(ids)), "Task IDs must be unique"
