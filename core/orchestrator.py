"""High-level coordinator for planner, executor and auditor."""


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

    def run(self, tasks_file: str = 'tasks.yml'):
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
        # Assuming memory.load_tasks returns a list of task objects
        tasks = self.memory.load_tasks(tasks_file)
        if tasks is None:
            tasks = [] # Start with an empty list if loading fails or file doesn't exist

        # Run reflection cycle
        # Assuming reflector.run_cycle takes tasks, potentially modifies them or adds new ones,
        # and returns the updated list of tasks.
        updated_tasks = self.reflector.run_cycle(tasks)
        if updated_tasks is not None:
            tasks = updated_tasks
        self.memory.save_tasks(tasks, tasks_file) # Save after reflection

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
