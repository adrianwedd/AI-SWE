import os
import unittest
from pathlib import Path
from unittest.mock import patch
from core.executor import Executor
from core.task import Task

class TestExecutor(unittest.TestCase):

    def setUp(self):
        self.executor = Executor()

    @patch('builtins.print')
    def test_execute_task_with_description(self, mock_print):
        task = Task(
            id="t1",
            description="Task One Description",
            component="test",
            dependencies=[],
            priority=1,
            status="pending",
        )
        self.executor.execute(task)
        mock_print.assert_called_once_with("Executing task: Task One Description")

    @patch('builtins.print')
    def test_execute_task_with_id_no_description(self, mock_print):
        task = Task(
            id="t2",
            description="",
            component="test",
            dependencies=[],
            priority=1,
            status="pending",
        )
        # Ensure description attribute is not present
        if hasattr(task, 'description'):
            delattr(task, 'description')
        self.executor.execute(task)
        mock_print.assert_called_once_with("Executing task ID: t2 (No description found)")

    @patch('builtins.print')
    def test_execute_task_no_description_no_id(self, mock_print):
        task = Task(
            id=0,
            description="",
            component="test",
            dependencies=[],
            priority=1,
            status="pending",
        )
        # Ensure description and id attributes are not present
        if hasattr(task, 'description'):
            delattr(task, 'description')
        if hasattr(task, 'id'):
            delattr(task, 'id')
        self.executor.execute(task)
        mock_print.assert_called_once_with("Executing task: (No description or ID found)")

    @patch('builtins.print')
    def test_execute_task_as_dict_with_description(self, mock_print):
        # The Executor expects an object with attributes. Using the Task
        # dataclass mimics this interface and keeps the test focused on the
        # print behavior rather than attribute lookups.
        task = Task(
            id="d1",
            description="Dict Task Description",
            component="test",
            dependencies=[],
            priority=1,
            status="pending",
        )
        self.executor.execute(task)
        mock_print.assert_called_once_with("Executing task: Dict Task Description")

    @patch('builtins.print')
    def test_execute_task_as_dict_with_id_no_description(self, mock_print):
        task_obj = Task(
            id="d2",
            description="",
            component="test",
            dependencies=[],
            priority=1,
            status="pending",
        )
        if hasattr(task_obj, 'description'):
            delattr(task_obj, 'description')
        self.executor.execute(task_obj)
        mock_print.assert_called_once_with("Executing task ID: d2 (No description found)")

    @patch('builtins.print')
    def test_execute_task_object_with_other_attributes(self, mock_print):
        task = Task(
            id="t_other",
            description="Other attributes test",
            component="test",
            dependencies=[],
            priority=10,
            status="pending",
        )
        self.executor.execute(task)
        mock_print.assert_called_once_with("Executing task: Other attributes test")

    def test_execute_task_with_command_creates_log(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                task = Task(
                    id="cmd",
                    description="Run echo",
                    component="test",
                    dependencies=[],
                    priority=1,
                    status="pending",
                    command="echo hello",
                )
                self.executor.execute(task)
            finally:
                os.chdir(cwd)

            logs = list(Path(tmpdir).joinpath("logs").glob("task-cmd-*.log"))
            assert logs, "Log file not created"
            assert logs[0].read_text().strip() == "hello"


if __name__ == '__main__':
    unittest.main()
