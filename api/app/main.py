from fastapi import FastAPI

from app.routes import auth, bookings, health, rooms
from app.store import Store, create_store_from_env


def create_app(store: Store | None = None) -> FastAPI:
    """
    Builds the FastAPI app. The store defaults to whatever the environment
    selects (SQLite locally, DynamoDB on AWS); tests can pass their own,
    e.g. create_sqlite_store(":memory:").
    """
    app = FastAPI(title="EscapeQueue API", version="1.0.0")
    app.state.store = store if store is not None else create_store_from_env()

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(rooms.router)
    app.include_router(bookings.router)

    return app
