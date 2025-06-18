"""Provide reflection utilities for self-improvement loops."""

from __future__ import annotations

from pathlib import Path
import yaml
from radon.complexity import cc_visit


class Reflector:
    """Perform a simple self-improvement cycle."""

    def __init__(
        self,
        tasks_path: Path | str = Path("tasks.yml"),
        threshold: int = 10,
        paths=None,
    ):
        self.tasks_path = Path(tasks_path)
        self.threshold = threshold
        self.paths = [Path(p) for p in paths] if paths else None

    # internal helpers
    def _load_tasks(self):
        if not self.tasks_path.exists():
            return []
        with self.tasks_path.open("r") as fh:
            return yaml.safe_load(fh) or []

    def _save_tasks(self, tasks):
        with self.tasks_path.open("w") as fh:
            yaml.safe_dump(tasks, fh, sort_keys=False)

    def _next_id(self, tasks):
        return max((t["id"] for t in tasks), default=0) + 1

    def _analyze(self, files):
        metrics = {}
        for path in files:
            try:
                text = Path(path).read_text()
            except OSError:
                continue
            blocks = cc_visit(text)
            total = sum(b.complexity for b in blocks)
            metrics[str(path)] = total
        return metrics

    def _decide(self, metrics, tasks):
        new_tasks = []
        next_id = self._next_id(tasks)
        for path, score in metrics.items():
            if score > self.threshold:
                new_tasks.append({
                    "id": next_id,
                    "description": f"Refactor {path} complexity {score}",
                    "component": "core",
                    "dependencies": [],
                    "priority": 3,
                    "status": "pending",
                })
                next_id += 1
        return new_tasks

    def run_cycle(self):
        files = self.paths or list(Path('.').rglob('*.py'))
        metrics = self._analyze(files)
        tasks = self._load_tasks()
        new_tasks = self._decide(metrics, tasks)
        if new_tasks:
            tasks.extend(new_tasks)
            self._save_tasks(tasks)
        return new_tasks
