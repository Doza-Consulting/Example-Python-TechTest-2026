"""
SQLite store (Python's built-in sqlite3, nothing to install).
Used for local development and tests. Pass ":memory:" for a throwaway DB.
"""

import os
import sqlite3
import threading
from typing import Any

from app.models import Booking, GameMaster, Room
from app.seed import SEED_GAME_MASTERS, seed_rooms
from app.store.base import Store

SCHEMA = """
CREATE TABLE IF NOT EXISTS rooms (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  theme TEXT NOT NULL,
  min_party_size INTEGER NOT NULL,
  max_party_size INTEGER NOT NULL,
  duration_minutes INTEGER NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS game_masters (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS bookings (
  id TEXT PRIMARY KEY,
  room_id TEXT NOT NULL,
  customer_name TEXT NOT NULL,
  party_size INTEGER NOT NULL,
  start_time TEXT NOT NULL,
  end_time TEXT NOT NULL,
  status TEXT NOT NULL,
  game_master_id TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
"""


class _Db:
    """One shared connection. FastAPI runs sync endpoints in a thread pool,
    so access is serialised with a lock."""

    def __init__(self, filename: str):
        if filename != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        self._conn = sqlite3.connect(filename, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        with self._lock:
            self._conn.executescript(SCHEMA)

    def query(self, sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self._conn.execute(sql, params).fetchall()

    def execute(self, sql: str, params: tuple[Any, ...] = ()) -> None:
        with self._lock:
            self._conn.execute(sql, params)
            self._conn.commit()


def _room(r: sqlite3.Row) -> Room:
    return Room(
        id=r["id"],
        name=r["name"],
        theme=r["theme"],
        min_party_size=r["min_party_size"],
        max_party_size=r["max_party_size"],
        duration_minutes=r["duration_minutes"],
        created_at=r["created_at"],
    )


def _game_master(r: sqlite3.Row) -> GameMaster:
    return GameMaster(id=r["id"], name=r["name"], email=r["email"])


def _booking(r: sqlite3.Row) -> Booking:
    return Booking(
        id=r["id"],
        room_id=r["room_id"],
        customer_name=r["customer_name"],
        party_size=r["party_size"],
        start_time=r["start_time"],
        end_time=r["end_time"],
        status=r["status"],
        game_master_id=r["game_master_id"],
        created_at=r["created_at"],
        updated_at=r["updated_at"],
    )


class _Rooms:
    def __init__(self, db: _Db):
        self._db = db

    def list(self) -> list[Room]:
        return [_room(r) for r in self._db.query("SELECT * FROM rooms ORDER BY name")]

    def get(self, id: str) -> Room | None:
        rows = self._db.query("SELECT * FROM rooms WHERE id = ?", (id,))
        return _room(rows[0]) if rows else None


class _GameMasters:
    def __init__(self, db: _Db):
        self._db = db

    def list(self) -> list[GameMaster]:
        return [_game_master(r) for r in self._db.query("SELECT * FROM game_masters ORDER BY name")]

    def get(self, id: str) -> GameMaster | None:
        rows = self._db.query("SELECT * FROM game_masters WHERE id = ?", (id,))
        return _game_master(rows[0]) if rows else None


class _Bookings:
    def __init__(self, db: _Db):
        self._db = db

    def list(self) -> list[Booking]:
        return [_booking(r) for r in self._db.query("SELECT * FROM bookings ORDER BY created_at")]

    def get(self, id: str) -> Booking | None:
        rows = self._db.query("SELECT * FROM bookings WHERE id = ?", (id,))
        return _booking(rows[0]) if rows else None

    def insert(self, b: Booking) -> None:
        self._db.execute(
            "INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                b.id,
                b.room_id,
                b.customer_name,
                b.party_size,
                b.start_time,
                b.end_time,
                b.status,
                b.game_master_id,
                b.created_at,
                b.updated_at,
            ),
        )

    def update(self, b: Booking) -> None:
        self._db.execute(
            """UPDATE bookings SET room_id = ?, customer_name = ?, party_size = ?,
                 start_time = ?, end_time = ?, status = ?, game_master_id = ?,
                 updated_at = ? WHERE id = ?""",
            (
                b.room_id,
                b.customer_name,
                b.party_size,
                b.start_time,
                b.end_time,
                b.status,
                b.game_master_id,
                b.updated_at,
                b.id,
            ),
        )


def create_sqlite_store(filename: str) -> Store:
    db = _Db(filename)

    # Seed reference data on first run.
    if db.query("SELECT COUNT(*) AS n FROM rooms")[0]["n"] == 0:
        for r in seed_rooms():
            db.execute(
                "INSERT INTO rooms VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    r.id,
                    r.name,
                    r.theme,
                    r.min_party_size,
                    r.max_party_size,
                    r.duration_minutes,
                    r.created_at,
                ),
            )
    if db.query("SELECT COUNT(*) AS n FROM game_masters")[0]["n"] == 0:
        for g in SEED_GAME_MASTERS:
            db.execute("INSERT INTO game_masters VALUES (?, ?, ?)", (g.id, g.name, g.email))

    return Store(rooms=_Rooms(db), game_masters=_GameMasters(db), bookings=_Bookings(db))
