import os
from pathlib import Path
import pytest


def test_artifacts_exist():
    required = ["ARCHITECTURE.md", "tasks.yml", "requirements.txt"]
    for fname in required:
        assert Path(fname).exists(), f"{fname} not found"


def test_log_created():
    logs = list(Path("logs").glob("bootstrap-*.log"))
    assert logs, "No bootstrap log found"
