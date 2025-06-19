import grpc
from . import io_service_pb2, io_service_pb2_grpc


def ping(message: str, host: str = "localhost", port: int = 50051) -> str:
    """Send a ping request to the Node IOService."""
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = io_service_pb2_grpc.IOServiceStub(channel)
    response = stub.Ping(io_service_pb2.PingRequest(message=message))
    return response.message
