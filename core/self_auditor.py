"""Utility to inspect executed tasks and gather metrics."""

from pathlib import Path

from radon.complexity import cc_visit
from radon.metrics import mi_visit


class SelfAuditor:
    """Inspect results of executed tasks."""

    def __init__(self, threshold: int = 10):
        self.threshold = threshold

    def analyze(self, root: str | Path = "core"):
        """Return maintainability metrics for Python files under ``root``."""
        root_path = Path(root)
        results: dict[str, dict[str, float]] = {}
        for pyfile in root_path.rglob("*.py"):
            try:
                code = pyfile.read_text()
            except OSError:
                continue
            mi = mi_visit(code, False)
            blocks = cc_visit(code)
            avg_cc = (
                sum(b.complexity for b in blocks) / len(blocks)
                if blocks
                else 0.0
            )
            results[str(pyfile)] = {"mi": mi, "avg_cc": avg_cc}
        return results

    def audit(self, root: str | Path = "core", tasks: list | None = None):
        """Return refactor tasks when complexity exceeds ``self.threshold``."""
        metrics = self.analyze(root)
        new = []
        next_id = 1
        if tasks:
            next_id = max((t.get("id", 0) for t in tasks), default=0) + 1
        for path, data in metrics.items():
            if data["avg_cc"] > self.threshold:
                new.append(
                    {
                        "id": next_id,
                        "description": f"Refactor {path} complexity {int(data['avg_cc'])}",
                        "component": "core",
                        "dependencies": [],
                        "priority": 3,
                        "status": "pending",
                    }
                )
                next_id += 1
        return new
