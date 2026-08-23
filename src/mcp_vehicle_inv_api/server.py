"""MCP server exposing the golang-api-example vehicle inventory API as tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from pydantic import ValidationError

from .models import VehicleDetailedRecord
from .vehicle_client import VehicleApiError, VehicleClient, VehicleNotFoundError

mcp = FastMCP("vehicle-inventory")
client = VehicleClient()


@mcp.tool()
async def add_vehicle(
    title: str,
    price: str,
    miles: int,
    inventory_added_date: str,
    vin: str,
    model: str,
    year: int,
    brand: str,
    type: str,
    exterior_color: str,
    interior_color: str,
    miles_per_gallon_city: int,
    miles_per_gallon_highway: int,
    transmission_type: str,
    cover_image_link: str = "",
    features: list[str] | None = None,
    exterior_image_links: list[str] | None = None,
    interior_image_links: list[str] | None = None,
    is_well_equipped: bool = False,
) -> dict:
    """Add a new vehicle to the inventory.

    inventory_added_date must be an ISO-8601 timestamp, e.g. "2024-03-10T09:00:00Z".
    Returns the generated stock_id on success.
    """
    try:
        record = VehicleDetailedRecord(
            title=title,
            price=price,
            miles=miles,
            cover_image_link=cover_image_link,
            inventory_added_date=inventory_added_date,
            vin=vin,
            model=model,
            year=year,
            brand=brand,
            type=type,
            exterior_color=exterior_color,
            interior_color=interior_color,
            miles_per_gallon_city=miles_per_gallon_city,
            miles_per_gallon_highway=miles_per_gallon_highway,
            transmission_type=transmission_type,
            features=features,
            exterior_image_links=exterior_image_links,
            interior_image_links=interior_image_links,
            is_well_equipped=is_well_equipped,
        )
    except ValidationError as e:
        return {"error": f"Invalid vehicle data: {e}"}

    try:
        return await client.add_vehicle(record.model_dump(mode="json", exclude_none=True))
    except VehicleApiError as e:
        return {"error": e.detail, "status_code": e.status_code}


@mcp.tool()
async def list_vehicles(offset: int = 0, limit: int = -1) -> dict:
    """List vehicles in inventory with pagination.

    offset: number of records to skip (default 0).
    limit: max records to return, -1 for all (default -1).
    """
    try:
        return await client.list_vehicles(offset=offset, limit=limit)
    except VehicleApiError as e:
        return {"error": e.detail, "status_code": e.status_code}


@mcp.tool()
async def get_vehicle_by_stock_id(stock_id: str) -> dict:
    """Get a single vehicle's full details by its stock ID."""
    try:
        return await client.get_vehicle_by_stock_id(stock_id)
    except VehicleNotFoundError as e:
        return {"error": e.detail, "status_code": e.status_code}
    except VehicleApiError as e:
        return {"error": e.detail, "status_code": e.status_code}


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
