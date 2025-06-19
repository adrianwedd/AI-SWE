from grafanalib.core import Dashboard, Graph, Row, Target
from grafanalib.prometheus import PromQL

DASHBOARD = Dashboard(
    title="AI-SWA Overview",
    rows=[
        Row(panels=[
            Graph(
                title="Tasks Executed",
                dataSource="Prometheus",
                targets=[Target(expr="tasks_executed_total", legendFormat="executed")],
            )
        ])
    ],
).auto_panel_ids()

if __name__ == "__main__":
    import json
    print(json.dumps(DASHBOARD.to_json_data(), indent=2))
