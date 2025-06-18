"""SelfAuditor analyzes code complexity and maintainability."""

from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Dict, List

from radon.complexity import cc_visit, cc_rank
from radon.metrics import mi_visit, mi_rank


class SelfAuditor:
    """Evaluate metrics and produce refactor tasks when thresholds are exceeded."""

    def __init__(self, complexity_threshold: int = 15, maintainability_threshold: str = "B") -> None:
        self.complexity_threshold = complexity_threshold
        self.maintainability_threshold = maintainability_threshold
        self.logger = logging.getLogger(__name__)

    # ------------------------------------------------------------------
    def analyze(self, paths: List[Path]) -> Dict[str, Dict]:
        """Return metrics for ``paths`` which should be Python files."""

        results: Dict[str, Dict] = {}
        for path in paths:
            if not path.exists() or path.suffix != ".py":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:  # pragma: no cover - IO issues
                self.logger.warning("Could not read %s: %s", path, exc)
                continue

            if not text.strip():
                continue

            file_metrics = self._analyze_file(str(path), text)
            results[str(path)] = file_metrics

        return results

    # ------------------------------------------------------------------
    def _analyze_file(self, filepath: str, content: str) -> Dict:
        try:
            ast.parse(content)
        except SyntaxError:
            return {"error": "Syntax error in file"}

        complexity_results = cc_visit(content)
        complexity_data = []
        max_complexity = 0

        for item in complexity_results:
            complexity = item.complexity
            rank = cc_rank(complexity)
            complexity_data.append(
                {
                    "name": item.name,
                    "complexity": complexity,
                    "rank": rank,
                    "lineno": item.lineno,
                    "type": item.classname or "function",
                }
            )
            max_complexity = max(max_complexity, complexity)

        try:
            mi_value = mi_visit(content, False)
            mi_rank_value = mi_rank(mi_value)
        except Exception:  # pragma: no cover - extremely unlikely
            mi_value = 0
            mi_rank_value = "F"

        needs_complexity_refactor = max_complexity > self.complexity_threshold
        needs_maintainability_refactor = self._rank_worse_than(
            mi_rank_value, self.maintainability_threshold
        )

        return {
            "complexity": complexity_data,
            "maintainability": {"mi": mi_value, "rank": mi_rank_value},
            "max_complexity": max_complexity,
            "needs_refactor": needs_complexity_refactor or needs_maintainability_refactor,
            "complexity_violations": [
                item for item in complexity_data if item["complexity"] > self.complexity_threshold
            ],
        }

    # ------------------------------------------------------------------
    def _rank_worse_than(self, current: str, threshold: str) -> bool:
        order = {"A": 1, "B": 2, "C": 3, "D": 4, "F": 5}
        return order.get(current, 5) > order.get(threshold, 2)

    # ------------------------------------------------------------------
    def _get_existing_refactor_files(self, existing_tasks: List[Dict]) -> set:
        files = set()
        for task in existing_tasks:
            desc = task.get("description", "")
            if "Refactor" in desc and desc.split():
                part = desc.split()[1]
                if part.endswith(".py"):
                    files.add(part)
            meta = task.get("metadata", {})
            if meta.get("type") == "refactor" and meta.get("filepath"):
                files.add(meta["filepath"])
        return files

    # ------------------------------------------------------------------
    def _calculate_priority(self, metrics: Dict) -> int:
        mc = metrics["max_complexity"]
        violations = len(metrics.get("complexity_violations", []))
        mi_rank_value = metrics["maintainability"]["rank"]

        if mc > 30:
            priority = 5
        elif mc > 20:
            priority = 4
        elif mc > 15:
            priority = 3
        else:
            priority = 2

        adjust = {"F": 1, "D": 0, "C": -1, "B": -1, "A": -2}
        priority += adjust.get(mi_rank_value, 0)

        if violations > 5:
            priority += 1

        return max(1, min(5, priority))

    # ------------------------------------------------------------------
    def audit(self, existing_tasks: List[Dict]) -> List[Dict]:
        """Analyze repository and return new refactor tasks."""

        python_files = [f for f in Path(".").rglob("*.py") if "__pycache__" not in str(f)]

        metrics = self.analyze(python_files)
        new_tasks: List[Dict] = []
        existing_refactor_files = self._get_existing_refactor_files(existing_tasks)

        max_id = max([t.get("id", 0) for t in existing_tasks], default=0)
        next_id = max_id + 1

        for filepath, file_metrics in metrics.items():
            if not file_metrics.get("needs_refactor"):
                continue
            if filepath in existing_refactor_files:
                continue

            max_complexity = file_metrics["max_complexity"]
            violations = file_metrics.get("complexity_violations", [])

            if violations:
                violation_details = (
                    f"Max complexity: {max_complexity}, Functions needing attention: {len(violations)}"
                )
            else:
                violation_details = f"Maintainability: {file_metrics['maintainability']['rank']}"

            task = {
                "id": next_id,
                "description": f"Refactor {filepath} - {violation_details}",
                "component": "refactor",
                "dependencies": [],
                "priority": self._calculate_priority(file_metrics),
                "status": "pending",
                "metadata": {
                    "type": "refactor",
                    "filepath": filepath,
                    "max_complexity": max_complexity,
                    "violations": len(violations),
                    "generated_by": "SelfAuditor",
                },
            }

            new_tasks.append(task)
            next_id += 1

        self.logger.info("Generated %d refactoring tasks", len(new_tasks))
        return new_tasks


if __name__ == "__main__":  # pragma: no cover - manual testing helper
    auditor = SelfAuditor()
    sample_files = list(Path(".").rglob("*.py"))[:5]
    metrics = auditor.analyze(sample_files)
    for file, data in metrics.items():
        print(f"\n{file}:")
        print(f"  Max Complexity: {data['max_complexity']}")
        print(f"  Needs Refactor: {data['needs_refactor']}")
        if data["complexity_violations"]:
            print(f"  Violations: {len(data['complexity_violations'])}")
