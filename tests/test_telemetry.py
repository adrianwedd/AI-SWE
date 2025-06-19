import requests
from core.telemetry import setup_telemetry


def test_setup_telemetry() -> None:
    server, _ = setup_telemetry(metrics_port=0)
    try:
        response = requests.get(f"http://localhost:{server.server_port}/metrics")
        assert response.status_code == 200
    finally:
        server.shutdown()
