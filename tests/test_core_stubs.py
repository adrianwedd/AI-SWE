import os
import types
from core.planner import Planner
from core.executor import Executor
from core.self_auditor import SelfAuditor

def test_planner_instantiation_and_plan():
    planner = Planner()
    assert planner.plan([]) is None

def test_executor_instantiation_and_execute(tmp_path):
    executor = Executor()
    task = types.SimpleNamespace(description="do nothing")
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        executor.execute(task)
    finally:
        os.chdir(cwd)

def test_self_auditor_instantiation_and_methods(tmp_path):
    sample = tmp_path / "example.py"
    sample.write_text("def foo():\n    return 1\n")
    auditor = SelfAuditor()
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        assert auditor.analyze([sample])
        result = auditor.audit([])
    finally:
        os.chdir(cwd)
    assert isinstance(result, list)
