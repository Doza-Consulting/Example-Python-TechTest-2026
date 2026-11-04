"""
Storage interface. The API only talks to this, so the same routes run
against SQLite locally and DynamoDB when deployed to AWS.

Methods: whole-collection `list()` plus get/insert/update. Any method you
add here needs implementing in every implementation under app/store/.
"""

from dataclasses import dataclass
from typing import Protocol

from app.models import Booking, GameMaster, Room


class RoomRepo(Protocol):
    def list(self) -> list[Room]: ...
    def get(self, id: str) -> Room | None: ...


class GameMasterRepo(Protocol):
    def list(self) -> list[GameMaster]: ...
    def get(self, id: str) -> GameMaster | None: ...


class BookingRepo(Protocol):
    def list(self) -> list[Booking]: ...
    def get(self, id: str) -> Booking | None: ...
    def insert(self, booking: Booking) -> None: ...
    def update(self, booking: Booking) -> None:
        """Replaces the stored booking with the same id."""
        ...


@dataclass
class Store:
    rooms: RoomRepo
    game_masters: GameMasterRepo
    bookings: BookingRepo
