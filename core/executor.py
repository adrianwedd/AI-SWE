class Executor:
    """
    A class responsible for executing tasks.
    """

    def execute(self, task: object) -> None:
        """
        Executes a given task.

        For now, this method simply prints the task's description
        to standard output. It assumes the task object has a 'description'
        attribute.

        Args:
            task: The task object to execute. Expected to have a
                  'description' attribute (e.g., task.description).
        """
        if hasattr(task, 'description'):
            print(f"Executing task: {task.description}")
        elif hasattr(task, 'id'):
            print(f"Executing task ID: {task.id} (No description found)")
        else:
            print("Executing task: (No description or ID found)")
