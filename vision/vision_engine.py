from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional

from core.task import Task


def wsjf_score(task: Task) -> float:
    """Return Weighted Shortest Job First score for ``task``."""
    cod = (
        getattr(task, "user_business_value", 0)
        + getattr(task, "time_criticality", 0)
        + getattr(task, "risk_reduction", 0)
    )
    job_size = getattr(task, "job_size", 1)
    if job_size == 0:
        job_size = 1
    return cod / job_size


@dataclass
class VisionEngine:
    """Prioritize tasks using WSJF with optional RL refinement."""

    rl_agent: Optional[RLAgent] = None
    shadow_mode: bool = True

    def prioritize(self, tasks: List[Task]) -> List[Task]:
        """Return ``tasks`` ordered by WSJF score."""
        scored = [(wsjf_score(t), t) for t in tasks]
        scored.sort(key=lambda x: x[0], reverse=True)
        ordered = [t for _, t in scored]
        if self.rl_agent:
            ordered = self._maybe_refine_with_rl(ordered)
        return ordered

    def _maybe_refine_with_rl(self, tasks: List[Task]) -> List[Task]:
        suggestions = self.rl_agent.suggest(tasks)
        if self.shadow_mode:
            # Log but do not alter ordering
            self.rl_agent.record_shadow_result(tasks, suggestions)
            return tasks
        return suggestions


class RLAgent:
    """Minimal stub of an RL agent for prioritization."""

    def __init__(self) -> None:
        self.history: List[Dict[str, List[int]]] = []

    def suggest(self, tasks: List[Task]) -> List[Task]:
        """Return refined ordering. Currently identity function."""
        return tasks

    def record_shadow_result(self, baseline: List[Task], suggestion: List[Task]) -> None:
        """Store comparison between baseline and suggestion for offline training."""
        self.history.append(
            {
                "baseline": [t.id for t in baseline],
                "suggestion": [t.id for t in suggestion],
            }
        )

    def train(self) -> None:  # pragma: no cover - placeholder for future training
        pass
