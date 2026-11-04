"""
Reference test showing the pattern: build the app with create_app() and
drive it in-process with FastAPI's TestClient (no port, no running server
needed). Each test gets its own throwaway in-memory SQLite store.
"""

from fastapi.testclient import TestClient

from app.main import create_app
from app.store.sqlite import create_sqlite_store


def test_health_returns_ok():
    client = TestClient(create_app(create_sqlite_store(":memory:")))

    res = client.get("/health")

    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
