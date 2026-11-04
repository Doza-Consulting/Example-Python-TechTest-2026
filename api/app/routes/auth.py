"""
Auth router: endpoints stubbed pending implementation.

Persistence goes through the store (see app/store/base.py); inject it with
`store: Store = Depends(get_store)` from app.deps.
"""

from fastapi import APIRouter

from app.errors import not_implemented

router = APIRouter()


@router.post("/auth/register")
def register():
    """
    TODO: register a new user.
    Should validate the input (name, email, password), reject an email that
    is already registered, and never store or return the plain-text password.
    """
    return not_implemented("POST /auth/register is not implemented yet.")


@router.post("/auth/login")
def login():
    """
    TODO: log a registered user in.
    Should check the credentials and return something the client can send
    on later requests to prove who they are.
    """
    return not_implemented("POST /auth/login is not implemented yet.")
