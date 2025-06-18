import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.self_auditor import SelfAuditor


def test_self_auditor_audit():
    auditor = SelfAuditor()
    result = auditor.audit()
    assert result is None
