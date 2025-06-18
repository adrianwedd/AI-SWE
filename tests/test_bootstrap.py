import os
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import pytest


def test_artifacts_exist():
    required = ["ARCHITECTURE.md", "tasks.yml", "requirements.txt", "AGENTS.md"]
    for fname in required:
        assert Path(fname).exists(), f"{fname} not found"


def test_log_created():
    logs = list(Path("logs").glob("bootstrap-*.log"))
    assert logs, "No bootstrap log found"


def test_missing_tasks_file(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "core" / "bootstrap.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2


def test_schema_error(tmp_path):
    (tmp_path / "tasks.yml").write_text("# jsonschema:\n# { invalid }")
    result = subprocess.run(
        [sys.executable, str(ROOT / "core" / "bootstrap.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
