import os
from pathlib import Path

from core.diff_utils import generate_diff, generate_file_diff


def test_generate_diff():
    diff = generate_diff("a\n", "b\n", "x")
    assert "-a" in diff and "+b" in diff


def test_generate_file_diff(tmp_path):
    file = tmp_path / "f.txt"
    file.write_text("old\n")
    diff = generate_file_diff(file, "new\n")
    assert "-old" in diff and "+new" in diff
