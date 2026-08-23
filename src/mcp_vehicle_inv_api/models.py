"""Pydantic models mirroring the golang-api-example vehicle records."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class VehicleDetailedRecord(BaseModel):
    """Request/response body for a single vehicle record.

    Mirrors models.VehicleDetailedRecord in golang-api-example. Fields such
    as stock_id, days_in_inventory, and is_under_warranty are generated or
    computed server-side and are not required on create.
    """

    title: str
    price: str
    miles: int
    cover_image_link: str = ""
    inventory_added_date: datetime
    vin: str
    model: str
    year: int
    brand: str
    type: str
    exterior_color: str
    interior_color: str
    miles_per_gallon_city: int
    miles_per_gallon_highway: int
    transmission_type: str
    features: list[str] | None = None
    exterior_image_links: list[str] | None = None
    interior_image_links: list[str] | None = None
    is_well_equipped: bool = False


class Vehicle(BaseModel):
    """Basic vehicle record as returned in list responses."""

    stock_id: str
    title: str
    price: str
    miles: int
    cover_image_link: str
    inventory_added_date: datetime
    days_in_inventory: int


class Metadata(BaseModel):
    offset: int
    limit: int
    total_count: int


class ListVehicleResponse(BaseModel):
    metadata: Metadata = Field(alias="_metadata")
    records: list[Vehicle] | None = None

    class Config:
        populate_by_name = True
