import subprocess
import sys
import os
from pathlib import Path


def test_cli_runs(tmp_path):
    cmd = [
        sys.executable,
        "-m",
        "core.cli",
        "--memory",
        str(tmp_path / "state.json"),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        cmd,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 0
    assert "Orchestrator running" in result.stdout


def test_cli_help(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [sys.executable, "-m", "core.cli", "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_cli_unwritable_memory(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "core.cli",
            "--memory",
            str(memory_dir),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode != 0
