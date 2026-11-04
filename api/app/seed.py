"""
Seed data. Written to the store on first start (SQLite locally, DynamoDB
when deployed) if the rooms / game masters tables are empty.
Bookings start empty and are created through the API.
"""

from datetime import datetime, timezone

from app.models import GameMaster, Room


def seed_rooms() -> list[Room]:
    created_at = datetime.now(timezone.utc).isoformat()
    return [
        Room(
            id="11111111-1111-1111-1111-111111111111",
            name="The Vault",
            theme="Heist",
            min_party_size=2,
            max_party_size=6,
            duration_minutes=60,
            created_at=created_at,
        ),
        Room(
            id="22222222-2222-2222-2222-222222222222",
            name="Cursed Manor",
            theme="Horror",
            min_party_size=3,
            max_party_size=8,
            duration_minutes=75,
            created_at=created_at,
        ),
        Room(
            id="33333333-3333-3333-3333-333333333333",
            name="Lost Signal",
            theme="Sci-Fi",
            min_party_size=2,
            max_party_size=4,
            duration_minutes=45,
            created_at=created_at,
        ),
    ]


SEED_GAME_MASTERS = [
    GameMaster(
        id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        name="Alex Rivera",
        email="alex@escapequeue.test",
    ),
    GameMaster(
        id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        name="Sam Okafor",
        email="sam@escapequeue.test",
    ),
]
