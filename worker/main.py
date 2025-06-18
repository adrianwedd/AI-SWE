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
            subprocess.run(command, shell=True, check=False)


if __name__ == "__main__":
    main()
