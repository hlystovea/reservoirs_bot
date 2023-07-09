from datetime import date

from pydantic import BaseModel


class Region(BaseModel):
    id: int
    url: str
    reservoirs: str
    name: str
    slug: str


class Reservoir(BaseModel):
    id: int
    url: str
    name: str
    slug: str
    water_situations: str
    actual_situation: str
    year_summary: str
    statistics_by_doy: str
    station_name: str | None
    force_level: float
    normal_level: float
    dead_level: float
    useful_volume: float | None
    full_volume: float | None
    area: float | None
    max_depth: float | None


class Situation(BaseModel):
    date: date
    level: float
    inflow: int | None
    avg_inflow: int | None
    outflow: int | None
    spillway: int | None
