"""Persistent storage utility for tasks and metadata."""

from pathlib import Path
import json
import yaml


class Memory:
    """Persist simple JSON state to disk."""

    def __init__(self, path: Path):
        """Initialize the memory store.

        Parameters
        ----------
        path:
            File location for the JSON state.
        """
        self.path = Path(path)

    def load(self):
        """Load and return persisted state or an empty dict."""
        if not self.path.exists():
            return {}
        with self.path.open("r") as fh:
            return json.load(fh)

    def save(self, data):
        """Persist ``data`` to disk as JSON."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w") as fh:
            json.dump(data, fh)

    # New helper methods for YAML task files
    def load_tasks(self, tasks_file: str):
        """Return tasks from a YAML file or an empty list."""
        path = Path(tasks_file)
        if not path.exists():
            return []
        with path.open("r") as fh:
            return yaml.safe_load(fh) or []

    def save_tasks(self, tasks, tasks_file: str):
        """Write tasks to ``tasks_file`` in YAML format."""
        path = Path(tasks_file)
        with path.open("w") as fh:
            yaml.safe_dump(tasks, fh, sort_keys=False)
