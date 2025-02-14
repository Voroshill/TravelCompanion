import httpx

from fastapi.responses import JSONResponse


def handle_http_error(error: httpx.HTTPStatusError):
    return JSONResponse(
        status_code=500,
        content={"error": f"HTTP error occurred: {error}"}
    )


def handle_request_error(error: httpx.RequestError):
    return JSONResponse(
        status_code=500,
        content={"error": f"Request error occurred: {error}"}
    )


def handle_unexpected_error(error: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"Unexpected error: {error}"}
    )
