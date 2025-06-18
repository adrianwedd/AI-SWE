from __future__ import annotations

from pathlib import Path
import difflib


def generate_diff(original: str, updated: str, filename: str = "file") -> str:
    """Return a unified diff for the given contents."""
    original_lines = original.splitlines(keepends=True)
    updated_lines = updated.splitlines(keepends=True)
    diff = difflib.unified_diff(
        original_lines,
        updated_lines,
        fromfile=f"{filename}.orig",
        tofile=f"{filename}.new",
    )
    return "".join(diff)


def generate_file_diff(path: Path, new_content: str) -> str:
    """Generate a diff between ``path`` on disk and ``new_content``."""
    if path.exists():
        old = path.read_text()
    else:
        old = ""
    return generate_diff(old, new_content, str(path))
