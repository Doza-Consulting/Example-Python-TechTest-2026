"""
Error responses use the shape { "error": { "code": ..., "message": ... } }
described in openapi.yaml.
"""

from fastapi.responses import JSONResponse


def error_body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


def not_implemented(message: str) -> JSONResponse:
    return JSONResponse(status_code=501, content=error_body("NOT_IMPLEMENTED", message))
