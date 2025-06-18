from __future__ import annotations

import subprocess
import shlex
from datetime import datetime
from pathlib import Path


class Executor:
    """Carry out tasks and capture their output."""

    def execute(self, task: object) -> None:
        """Execute ``task`` and write any command output to ``logs/``.

        If the task defines a ``command`` attribute, it will be executed in a
        subprocess. The combined stdout and stderr are written to a timestamped
        log file under ``logs/``.

        Parameters
        ----------
        task:
            Object representing the task to execute. It may define
            ``description`` and/or ``command`` attributes.
        """

        if hasattr(task, "description"):
            print(f"Executing task: {task.description}")
        elif hasattr(task, "id"):
            print(f"Executing task ID: {task.id} (No description found)")
        else:
            print("Executing task: (No description or ID found)")

        command = getattr(task, "command", None)
        if not command:
            return

        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"task-{getattr(task, 'id', 'unknown')}-{timestamp}.log"
        log_file.write_text(result.stdout + result.stderr)
