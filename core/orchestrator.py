"""High-level coordinator for planner, executor and auditor."""


class Orchestrator:
    """Coordinate planner, executor, auditor and persistence."""

    def __init__(self, planner, executor, auditor, memory):
        """Create a new orchestrator instance.

        Parameters
        ----------
        planner, executor, auditor:
            Components responsible for planning, execution and auditing.
        memory:
            ``Memory`` instance used for persistence.
        """
        self.planner = planner
        self.executor = executor
        self.auditor = auditor
        self.memory = memory

    def run(self):
        """Execute a single orchestration cycle and return ``True``."""
        print("Orchestrator running")
        # Future logic will coordinate components using memory
        return True
