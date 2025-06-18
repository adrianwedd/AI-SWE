import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.planner import Planner  # noqa: E402


def test_planner_plan():
    planner = Planner()
    result = planner.plan([])
    assert result is None
