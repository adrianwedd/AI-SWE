from __future__ import annotations

"""Simple RL training pipeline for the Vision Engine."""

from dataclasses import dataclass

from core.observability import MetricsProvider
from .vision_engine import RLAgent


@dataclass
class RLTrainer:
    """Train an :class:`RLAgent` using observability metrics."""

    agent: RLAgent
    metrics_provider: MetricsProvider

    def run(self) -> None:
        """Collect metrics and pass them to the agent's training routine."""
        metrics = self.metrics_provider.collect()
        self.agent.train(metrics)
