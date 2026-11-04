"""
Bookings router: all endpoints stubbed pending implementation.

No auth and no validation yet. Persistence goes through the store (see
app/store/base.py); inject it with `store: Store = Depends(get_store)`.
"""

from fastapi import APIRouter

from app.errors import not_implemented

router = APIRouter()


@router.get("/bookings")
def list_bookings():
    """
    TODO: list bookings.
    Should support filtering (roomId, status) and pagination.
    Should require authentication.
    """
    return not_implemented("GET /bookings is not implemented yet.")


@router.post("/bookings")
def create_booking():
    """
    TODO: create a booking.
    Should validate party_size against the room's min/max capacity and
    reject any request that overlaps an existing confirmed booking for the
    same room. Should require authentication.
    """
    return not_implemented("POST /bookings is not implemented yet.")


@router.get("/bookings/{booking_id}")
def get_booking(booking_id: str):
    """
    TODO: fetch a single booking by id. Should require authentication.
    """
    return not_implemented("GET /bookings/{id} is not implemented yet.")


@router.patch("/bookings/{booking_id}")
def update_booking(booking_id: str):
    """
    TODO: update a booking (reschedule, change party size, cancel).
    Should require authentication; reschedules should be checked against
    the same overlap rule as creation.
    """
    return not_implemented("PATCH /bookings/{id} is not implemented yet.")


@router.post("/bookings/{booking_id}/assign")
def assign_game_master(booking_id: str):
    """
    TODO: assign a game master to a booking by gameMasterId.
    Should require authentication.
    """
    return not_implemented("POST /bookings/{id}/assign is not implemented yet.")
