"""Command-line worker that polls the broker for pending tasks.

The script contacts the broker specified by ``BROKER_URL`` and retrieves any
pending tasks. Each task may provide a shell ``command`` which is executed in
an isolated subprocess. The worker then posts the command's ``stdout``,
``stderr`` and ``exit_code`` back to the broker.
"""

import os
import requests
import subprocess
from core.telemetry import setup_telemetry

BROKER_URL = os.environ.get("BROKER_URL", "http://broker:8000")
setup_telemetry(service_name="worker", metrics_port=int(os.getenv("METRICS_PORT", "9001")))


def fetch_tasks():
    api_key = os.getenv("API_KEY")
    headers = {"X-API-Key": api_key} if api_key else {}
    resp = requests.get(f"{BROKER_URL}/tasks", headers=headers)
    resp.raise_for_status()
    return resp.json()


def main():
    tasks = fetch_tasks()
    for task in tasks:
        command = task.get("command")
        if command:
            result = subprocess.run(
                command, shell=True, check=False, capture_output=True, text=True
            )
            api_key = os.getenv("API_KEY")
            headers = {"X-API-Key": api_key} if api_key else {}
            requests.post(
                f"{BROKER_URL}/tasks/{task['id']}/result",
                json={
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode,
                },
                headers=headers,
            ).raise_for_status()


if __name__ == "__main__":
    main()
