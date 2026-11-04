"""FastAPI dependencies shared by the routers."""

from fastapi import Request

from app.store import Store


def get_store(request: Request) -> Store:
    """The store the app was built with. Use as `store: Store = Depends(get_store)`."""
    return request.app.state.store
