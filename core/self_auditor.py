"""Utility to inspect executed tasks and gather metrics."""

from pathlib import Path

from radon.complexity import cc_visit
from radon.metrics import mi_visit


class SelfAuditor:
    """Inspect results of executed tasks."""

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

    def audit(self):
        """Perform an audit step."""
        pass
