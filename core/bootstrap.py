import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import validate, ValidationError


def load_schema_and_tasks(path: Path):
    try:
        text = path.read_text()
    except OSError as exc:
        logging.error("[ERROR] %s", exc)
        sys.exit(2)

    schema_lines = []
    task_lines = []
    lines = text.splitlines()
    schema_started = False
    for line in lines:
        if line.startswith("# jsonschema:"):
            schema_started = True
            continue
        if schema_started and line.startswith("#"):
            schema_lines.append(line[1:].lstrip())
            continue
        task_lines.append(line)

    schema_str = "\n".join(schema_lines)
    try:
        schema = json.loads(schema_str)
    except json.JSONDecodeError as exc:
        logging.error("[ERROR] %s", exc)
        sys.exit(1)

    try:
        tasks = yaml.safe_load("\n".join(task_lines)) or []
    except yaml.YAMLError as exc:
        logging.error("[ERROR] %s", exc)
        sys.exit(1)

    return schema, tasks


def main():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    logfile = Path("logs") / f"bootstrap-{timestamp}.log"
    try:
        logfile.parent.mkdir(exist_ok=True)
        logging.basicConfig(filename=logfile, level=logging.INFO)
    except OSError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(2)

    schema, tasks = load_schema_and_tasks(Path("tasks.yml"))

    try:
        validate(instance=tasks, schema=schema)
    except ValidationError as exc:
        logging.error("[ERROR] %s", exc)
        sys.exit(1)

    pending = [t for t in tasks if t.get("status") == "pending"]
    if not pending:
        logging.info("No pending tasks found")
        sys.exit(0)

    task = sorted(pending, key=lambda x: x.get("priority", 5))[0]
    logging.info("Next task: %s", task)
    sys.exit(0)


if __name__ == "__main__":
    main()
