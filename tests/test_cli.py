import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_cli_runs(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "core.cli", "--memory", str(tmp_path / "state.json")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Orchestrator running" in result.stdout
