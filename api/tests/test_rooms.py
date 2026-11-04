from fastapi.testclient import TestClient

from app.main import create_app
from app.store.sqlite import create_sqlite_store


def test_list_rooms_returns_the_seeded_rooms():
    client = TestClient(create_app(create_sqlite_store(":memory:")))

    res = client.get("/rooms")

    assert res.status_code == 200
    assert [r["name"] for r in res.json()["data"]] == ["Cursed Manor", "Lost Signal", "The Vault"]
    assert res.json()["data"][0]["minPartySize"] == 3
