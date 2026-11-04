"""
Picks a store implementation from the environment:

  STORAGE=sqlite   (default) local file DB at SQLITE_PATH (default ./data/escapequeue.db)
  STORAGE=dynamodb           DynamoDB tables named `${TABLE_PREFIX}-...`
"""

import os

from app.store.base import Store

__all__ = ["Store", "create_store_from_env"]


def create_store_from_env() -> Store:
    kind = os.environ.get("STORAGE", "sqlite")

    if kind == "dynamodb":
        prefix = os.environ.get("TABLE_PREFIX")
        if not prefix:
            raise RuntimeError("TABLE_PREFIX is required when STORAGE=dynamodb")
        # Imported lazily so each runtime only loads the driver it uses.
        from app.store.dynamodb import create_dynamo_store

        return create_dynamo_store(prefix)

    if kind == "sqlite":
        from app.store.sqlite import create_sqlite_store

        return create_sqlite_store(os.environ.get("SQLITE_PATH", "./data/escapequeue.db"))

    raise RuntimeError(f'Unknown STORAGE "{kind}" (expected "sqlite" or "dynamodb")')
