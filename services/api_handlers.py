import datetime as dt

from pydantic import parse_obj_as

from services.schemas import Region, Reservoir, Situation
from services.client import client

REGIONS_PATH = '/api/v1/regions/'
RESERVOIRS_PATH = '/api/v1/reservoirs/'


async def get_regions() -> list[Region]:
    async with client.get_session() as session:
        async with session.get(REGIONS_PATH) as resp:
            data = await resp.json()
    return parse_obj_as(list[Region], data)


async def get_reservoirs(region: str) -> list[Reservoir]:
    params = {'region': region}
    async with client.get_session() as session:
        async with session.get('/api/v1/reservoirs/', params=params) as resp:
            data = await resp.json()
    return parse_obj_as(list[Reservoir], data)


async def get_reservoir(id: int) -> Reservoir:
    async with client.get_session() as session:
        async with session.get(f'{RESERVOIRS_PATH}{id}/') as resp:
            data = await resp.json()
    return Reservoir(**data)


async def get_situations(
    reservoir_id: int, start: dt.date, end: dt.date
) -> list[Situation]:
    params = {
        'start': start.isoformat(),
        'end': end.isoformat(),
    }
    async with client.get_session() as session:
        async with session.get(
            f'/api/v1/reservoirs/{reservoir_id}/situations/',
            params=params
        ) as resp:
            data = await resp.json()
    return parse_obj_as(list[Situation], data)
