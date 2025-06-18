import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.self_auditor import SelfAuditor  # noqa: E402


def test_self_auditor_audit(tmp_path):
    pyfile = tmp_path / "sample.py"
    pyfile.write_text(
        "def foo(x):\n    if x > 1:\n        return 1\n    else:\n        return 0\n"
    )
    auditor = SelfAuditor(complexity_threshold=1)

    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        new_tasks = auditor.audit([])
    finally:
        os.chdir(cwd)

    assert new_tasks
    assert new_tasks[0]["metadata"]["type"] == "refactor"


def test_self_auditor_analyze(tmp_path):
    target = tmp_path / "sample.py"
    target.write_text("def foo():\n    return 1\n")
    auditor = SelfAuditor()
    metrics = auditor.analyze([target])
    key = str(target)
    assert key in metrics
    assert metrics[key]["maintainability"]["mi"] > 0
