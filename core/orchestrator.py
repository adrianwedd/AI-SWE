"""High-level coordinator for planner, executor and auditor."""

from typing import List
from dataclasses import asdict
from .task import Task


class Orchestrator:
    """
    Coordinates the self-improving loop of task planning, execution, and reflection.
    """

    def __init__(self, planner, executor, reflector, memory):
        """
        Initializes the Orchestrator with necessary components.

        Args:
            planner: An instance of the Planner class.
            executor: An instance of the Executor class.
            reflector: An instance of the Reflector class.
            memory: An instance of the Memory class for loading/saving tasks.
        """
        self.planner = planner
        self.executor = executor
        self.reflector = reflector
        self.memory = memory

    def run(self, tasks_file: str = 'tasks.yml') -> None:
        """
        Runs the main orchestration loop.

        The loop consists of:
        1. Loading tasks.
        2. Running a reflection cycle to potentially add/modify tasks.
        3. Iteratively planning, executing, and updating task statuses.

        Args:
            tasks_file (str): The name of the file from which to load and
                              to which to save tasks. Defaults to 'tasks.yml'.
        """
        # Load initial tasks
        # Load persisted tasks as ``Task`` objects
        tasks: List[Task] = self.memory.load_tasks(tasks_file)
        if tasks is None:
            tasks = [] # Start with an empty list if loading fails or file doesn't exist

        # Run reflection cycle
        # Assuming reflector.run_cycle takes tasks, potentially modifies them or adds new ones,
        # and returns the updated list of tasks.
        def _to_dict(t: Task) -> dict:
            return {f: getattr(t, f) for f in Task.__dataclass_fields__ if hasattr(t, f)}

        reflected = self.reflector.run_cycle([_to_dict(t) for t in tasks])
        if reflected is not None:
            if reflected and isinstance(reflected[0], Task):
                tasks = reflected
            else:
                fields = set(Task.__dataclass_fields__.keys())
                tasks = [Task(**{k: v for k, v in item.items() if k in fields}) for item in reflected]
        self.memory.save_tasks(tasks, tasks_file)  # Save after reflection

        while True:
            next_task = self.planner.plan(tasks)

            if next_task is None:
                # No actionable tasks left (all done or blocked)
                print("Orchestrator: No actionable tasks. Halting.")
                break

            print(f"Orchestrator: Task '{getattr(next_task, 'id', 'N/A')}' selected for execution.")

            # Mark task as "in_progress"
            # Assuming task objects are mutable and have a 'status' attribute
            if hasattr(next_task, 'status'):
                next_task.status = "in_progress"
                self.memory.save_tasks(tasks, tasks_file)
            else:
                print(
                    f"Warning: Task '{getattr(next_task, 'id', 'N/A')}' has no 'status' attribute."
                )

            # Execute the task
            print(f"Orchestrator: Executing task '{getattr(next_task, 'id', 'N/A')}'.")
            self.executor.execute(next_task)

            # Mark task as "done"
            if hasattr(next_task, 'status'):
                next_task.status = "done"
                self.memory.save_tasks(tasks, tasks_file)
            else:
                # This case should ideally not happen if it had status for "in_progress"
                print(
                    f"Warning: Task '{getattr(next_task, 'id', 'N/A')}' has no 'status' attribute to mark as done."
                )

            print(f"Orchestrator: Task '{getattr(next_task, 'id', 'N/A')}' completed.")

        print("Orchestrator: Run finished.")
