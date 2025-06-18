"""Persistent storage utility for tasks and metadata."""

from pathlib import Path
import json


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
