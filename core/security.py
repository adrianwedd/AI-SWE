"""Minimal security utilities for microservices."""

from __future__ import annotations

import os
from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str | None = Header(None)) -> None:
    """Verify the ``X-API-Key`` header if ``API_KEY`` is configured."""
    api_key = os.getenv("API_KEY")
    if api_key and x_api_key != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
