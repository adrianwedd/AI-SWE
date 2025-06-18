import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.self_auditor import SelfAuditor  # noqa: E402


def test_self_auditor_audit():
    auditor = SelfAuditor()
    result = auditor.audit()
    assert result is None


def test_self_auditor_analyze(tmp_path):
    target = tmp_path / "sample.py"
    target.write_text("def foo():\n    return 1\n")
    auditor = SelfAuditor()
    metrics = auditor.analyze(tmp_path)
    key = str(target)
    assert key in metrics
    assert metrics[key]["mi"] > 0
