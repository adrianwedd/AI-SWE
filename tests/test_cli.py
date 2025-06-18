import subprocess
import sys


def test_cli_runs(tmp_path):
    cmd = [
        sys.executable,
        "-m",
        "core.cli",
        "--memory",
        str(tmp_path / "state.json"),
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Orchestrator running" in result.stdout
