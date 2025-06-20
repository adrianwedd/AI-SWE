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
    code_file.write_text("""\
def func(x):
    if x > 0:
        if x > 1:
            return 1
        else:
            return 2
    else:
        return 3
""")
    refl = Reflector(tasks_path=tasks_file, complexity_threshold=1, analysis_paths=[code_file])
    tasks = yaml.safe_load(tasks_file.read_text())
    result = refl.run_cycle(tasks)
    assert isinstance(result, list)
    updated = yaml.safe_load(tasks_file.read_text())
    assert isinstance(updated, list)

from core.observability import MetricsProvider


def test_reflector_collects_metrics(tmp_path):
    tasks_file = tmp_path / "tasks.yml"
    tasks_file.write_text(
        "- id: 1\n"
        "  description: base\n"
        "  component: core\n"
        "  dependencies: []\n"
        "  priority: 1\n"
        "  status: pending\n"
    )
    code_file = tmp_path / "code.py"
    code_file.write_text("def foo():\n    return 1\n")
    metrics_file = tmp_path / "metrics.json"
    metrics_file.write_text('{"coverage": 90}')

    provider = MetricsProvider(metrics_file)
    refl = Reflector(
        tasks_path=tasks_file,
        complexity_threshold=1,
        analysis_paths=[code_file],
        metrics_provider=provider,
    )
    analysis = refl.analyze()
    assert analysis.get("observability_metrics") == {"coverage": 90}

