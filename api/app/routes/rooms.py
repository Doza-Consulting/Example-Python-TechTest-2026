"""
Rooms router.
"""

from fastapi import APIRouter, Depends

from app.deps import get_store
from app.errors import not_implemented
from app.models import Room
from app.store import Store

router = APIRouter()


@router.get("/rooms")
def list_rooms(store: Store = Depends(get_store)) -> dict[str, list[Room]]:
    """List all rooms. Implemented."""
    return {"data": store.rooms.list()}


@router.get("/rooms/{room_id}/availability")
def room_availability(room_id: str):
    """
    TODO: Implement this endpoint.

    Must be public (no auth) and must not expose booking/customer detail,
    only slot start/end times and availability. Should honor optional
    `from` / `to` query params (ISO 8601 date-times) if provided. Should
    return 404 if the room doesn't exist.

    See openapi.yaml for the full response contract (AvailabilitySlot).
    """
    return not_implemented("GET /rooms/{id}/availability is not implemented yet.")
