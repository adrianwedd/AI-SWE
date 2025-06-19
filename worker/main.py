"""Command-line worker that polls the broker for pending tasks.

The script contacts the broker specified by ``BROKER_URL`` and retrieves any
pending tasks. Each task may provide a shell ``command`` which is executed in
an isolated subprocess. The worker then posts the command's ``stdout``,
``stderr`` and ``exit_code`` back to the broker.
"""

import os
import requests
import subprocess

BROKER_URL = os.environ.get("BROKER_URL", "http://broker:8000")


def fetch_tasks():
    resp = requests.get(f"{BROKER_URL}/tasks")
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
            requests.post(
                f"{BROKER_URL}/tasks/{task['id']}/result",
                json={
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode,
                },
            ).raise_for_status()


if __name__ == "__main__":
    main()
