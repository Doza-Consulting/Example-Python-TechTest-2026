"""
DynamoDB store, used when the API is deployed to AWS (see /terraform).

One on-demand table per entity, keyed on `id`, named `${prefix}-rooms`,
`${prefix}-game-masters` and `${prefix}-bookings`. Items are stored as the
plain model fields (snake_case). `list()` is a Scan, which is fine at this
scale.
"""

from typing import Any, Callable, TypeVar

import boto3

from app.models import ApiModel, Booking, GameMaster, Room
from app.seed import SEED_GAME_MASTERS, seed_rooms
from app.store.base import Store

M = TypeVar("M", bound=ApiModel)


def create_dynamo_store(table_prefix: str) -> Store:
    dynamodb = boto3.resource("dynamodb")

    def table(name: str):
        return dynamodb.Table(f"{table_prefix}-{name}")

    def scan(name: str, model: type[M]) -> list[M]:
        tbl = table(name)
        items: list[dict[str, Any]] = []
        kwargs: dict[str, Any] = {}
        while True:
            res = tbl.scan(**kwargs)
            items.extend(res.get("Items", []))
            if "LastEvaluatedKey" not in res:
                break
            kwargs["ExclusiveStartKey"] = res["LastEvaluatedKey"]
        return [model.model_validate(i) for i in items]

    def get(name: str, model: type[M], id: str) -> M | None:
        item = table(name).get_item(Key={"id": id}).get("Item")
        return model.model_validate(item) if item else None

    def put(name: str, item: ApiModel) -> None:
        table(name).put_item(Item=item.model_dump())

    seeded = False

    def ensure_seeded() -> None:
        """Seed reference data once per container, only if the table is empty."""
        nonlocal seeded
        if seeded:
            return
        if not scan("rooms", Room):
            for r in seed_rooms():
                put("rooms", r)
        if not scan("game-masters", GameMaster):
            for g in SEED_GAME_MASTERS:
                put("game-masters", g)
        seeded = True

    def seeding(fn: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            ensure_seeded()
            return fn(*args, **kwargs)

        return wrapper

    class _Rooms:
        @seeding
        def list(self) -> list[Room]:
            return sorted(scan("rooms", Room), key=lambda r: r.name)

        @seeding
        def get(self, id: str) -> Room | None:
            return get("rooms", Room, id)

    class _GameMasters:
        @seeding
        def list(self) -> list[GameMaster]:
            return sorted(scan("game-masters", GameMaster), key=lambda g: g.name)

        @seeding
        def get(self, id: str) -> GameMaster | None:
            return get("game-masters", GameMaster, id)

    class _Bookings:
        def list(self) -> list[Booking]:
            return sorted(scan("bookings", Booking), key=lambda b: b.created_at)

        def get(self, id: str) -> Booking | None:
            return get("bookings", Booking, id)

        def insert(self, booking: Booking) -> None:
            put("bookings", booking)

        def update(self, booking: Booking) -> None:
            put("bookings", booking)

    return Store(rooms=_Rooms(), game_masters=_GameMasters(), bookings=_Bookings())
