import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402

import yaml  # noqa: E402
from core.reflector import Reflector  # noqa: E402


def test_reflector_creates_task(tmp_path):
    tasks_file = tmp_path / "tasks.yml"
    tasks_file.write_text(
        "- id: 1\n"
        "  description: base\n"
        "  component: core\n"
        "  dependencies: []\n"
        "  priority: 1\n"
        "  status: pending\n"
    )
    code_file = tmp_path / "complex.py"
    code_file.write_text(
        """\
def func(x):
    if x > 0:
        if x > 1:
            return 1
        else:
            return 2
    else:
        return 3
"""
    )
    refl = Reflector(tasks_path=tasks_file, threshold=1, paths=[code_file])
    new_tasks = refl.run_cycle()
    assert new_tasks
    tasks = yaml.safe_load(tasks_file.read_text())
    assert len(tasks) == 2
    assert tasks[-1]["description"].startswith("Refactor")
