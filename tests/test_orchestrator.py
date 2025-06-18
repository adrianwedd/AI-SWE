import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.orchestrator import Orchestrator  # noqa: E402
from core.memory import Memory  # noqa: E402


def test_orchestrator_run(capsys, tmp_path):
    mem = Memory(tmp_path / "state.json")
    orch = Orchestrator(None, None, None, mem)
    result = orch.run()
    captured = capsys.readouterr()
    assert result is True
    assert "Orchestrator running" in captured.out
