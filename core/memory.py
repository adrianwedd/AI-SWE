from pathlib import Path
import json


class Memory:
    """Persist simple JSON state to disk."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return {}
        with self.path.open("r") as fh:
            return json.load(fh)

    def save(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w") as fh:
            json.dump(data, fh)
