import os
from importlib import reload
from pathlib import Path

from fastapi.testclient import TestClient

# Set DB_PATH before importing the broker

def setup_module(module):
    os.environ["DB_PATH"] = str(Path(module.__file__).parent / "test.db")
    global broker
    import broker.main as broker_module
    broker = reload(broker_module)


def test_create_and_get_task(tmp_path):
    os.environ["DB_PATH"] = str(tmp_path / "api.db")
    broker = reload(__import__("broker.main", fromlist=["app", "init_db"]))
    client = TestClient(broker.app)

    resp = client.post("/tasks", json={"description": "demo"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["description"] == "demo"
    task_id = data["id"]

    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == task_id
