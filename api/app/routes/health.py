"""
Health check endpoint, already implemented and working.

This is here as a reference for the pattern the rest of the app follows
(router per resource, JSON responses, standard FastAPI routing). Nothing
to build here.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
