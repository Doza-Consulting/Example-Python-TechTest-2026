"""
Domain types shared by the API, the storage layer and the seed data.

Fields are snake_case in Python and camelCase in JSON (see openapi.yaml).
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Room(ApiModel):
    id: str
    name: str
    theme: str
    min_party_size: int
    max_party_size: int
    duration_minutes: int
    created_at: str


class GameMaster(ApiModel):
    id: str
    name: str
    email: str


BookingStatus = Literal["confirmed", "cancelled"]


class Booking(ApiModel):
    id: str
    room_id: str
    customer_name: str
    party_size: int
    start_time: str
    end_time: str
    status: BookingStatus
    game_master_id: str | None
    created_at: str
    updated_at: str
