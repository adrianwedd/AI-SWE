import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.executor import Executor


def test_executor_execute():
    executor = Executor()
    result = executor.execute(None)
    assert result is None
