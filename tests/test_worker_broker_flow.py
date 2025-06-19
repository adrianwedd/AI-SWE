import os
import sqlite3
from importlib import reload
from types import SimpleNamespace

from fastapi.testclient import TestClient

import broker.main as broker_module
import worker.main as worker_module


def setup_broker(tmp_path):
    os.environ["DB_PATH"] = str(tmp_path / "api.db")
    os.environ["METRICS_PORT"] = "0"
    broker = reload(broker_module)
    return TestClient(broker.app)


def run_worker(client, monkeypatch):
    os.environ["BROKER_URL"] = str(client.base_url)
    os.environ["METRICS_PORT"] = "0"
    mod = reload(worker_module)

    def _get(url, *args, **kwargs):
        return client.get(url.replace(str(client.base_url), ""))

    def _post(url, *args, **kwargs):
        return client.post(url.replace(str(client.base_url), ""), json=kwargs.get("json"))

    monkeypatch.setattr(mod, "requests", SimpleNamespace(get=_get, post=_post))
    mod.main()


def fetch_result(db_path, task_id):
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT stdout, stderr, exit_code FROM task_results WHERE task_id=?",
        (task_id,),
    ).fetchone()
    conn.close()
    return row


def test_worker_success_result(tmp_path, monkeypatch):
    client = setup_broker(tmp_path)
    resp = client.post("/tasks", json={"description": "demo", "command": "echo hi"})
    task_id = resp.json()["id"]
    run_worker(client, monkeypatch)
    stdout, stderr, code = fetch_result(str(tmp_path / "api.db"), task_id)
    assert stdout.strip() == "hi"
    assert stderr == ""
    assert code == 0


def test_worker_failure_result(tmp_path, monkeypatch):
    client = setup_broker(tmp_path)
    cmd = "sh -c 'echo fail >&2; exit 1'"
    resp = client.post("/tasks", json={"description": "fail", "command": cmd})
    task_id = resp.json()["id"]
    run_worker(client, monkeypatch)
    stdout, stderr, code = fetch_result(str(tmp_path / "api.db"), task_id)
    assert code != 0
    assert "fail" in stderr
