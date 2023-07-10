from datetime import date

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Region(BaseOrjsonModel):
    id: int
    url: str
    reservoirs: str
    name: str
    slug: str


class Reservoir(BaseOrjsonModel):
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


class Situation(BaseOrjsonModel):
    date: date
    level: float
    inflow: int | None
    avg_inflow: int | None
    outflow: int | None
    spillway: int | None
