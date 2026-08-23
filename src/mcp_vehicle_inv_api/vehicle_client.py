"""HTTP client for the golang-api-example vehicle inventory API."""

from __future__ import annotations

import os

import httpx

DEFAULT_BASE_URL = "http://localhost:3001/inventory/v1"


class VehicleApiError(Exception):
    """Raised when the golang-api-example vehicle API returns an error response."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"[{status_code}] {detail}")


class VehicleNotFoundError(VehicleApiError):
    """Raised when a vehicle with the given stock ID does not exist."""


class VehicleClient:
    """Thin async wrapper around the vehicle inventory REST API."""

    def __init__(self, base_url: str | None = None, timeout: float = 10.0):
        self._base_url = (base_url or os.environ.get("GOLANG_API_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout

    async def add_vehicle(self, vehicle: dict) -> dict:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(f"{self._base_url}/vehicles", json=vehicle)
        self._raise_for_status(resp)
        return resp.json()

    async def list_vehicles(self, offset: int = 0, limit: int = -1) -> dict:
        params = {"offset": offset, "limit": limit}
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.get(f"{self._base_url}/vehicles", params=params)
        self._raise_for_status(resp)
        return resp.json()

    async def get_vehicle_by_stock_id(self, stock_id: str) -> dict:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.get(f"{self._base_url}/vehicles/{stock_id}")
        if resp.status_code == 404:
            raise VehicleNotFoundError(404, f"No vehicle found for stock_id={stock_id}")
        self._raise_for_status(resp)
        return resp.json()

    @staticmethod
    def _raise_for_status(resp: httpx.Response) -> None:
        if resp.is_success:
            return
        detail = resp.text
        try:
            body = resp.json()
            detail = body.get("detail", detail)
        except ValueError:
            pass
        raise VehicleApiError(resp.status_code, detail)
