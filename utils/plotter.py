import datetime as dt
import io
import logging
from typing import Iterable, List, Tuple

import matplotlib.pyplot as plt
from peewee_async import AsyncQueryWrapper, Manager

from bot.exceptions import NoDataError
from db.models import database, ReservoirModel, SituationModel


objects = Manager(database)
objects.database.allow_sync = logging.ERROR


Y_LABEL = {
    'level': 'Высота над уровнем моря, м',
    'flows': 'Q, м\u00b3/с',
}

PARAMS = {
    'level': {
        'color': '#ff9f40',
        'label': 'УВБ (м)',
    },
    'inflow': {
        'color': '#ff6384',
        'label': 'Приток (м\u00b3/c)',
    },
    'outflow': {
        'color': '#36a2eb',
        'label': 'Сброс (м\u00b3/c)',
    },
    'spillway': {
        'color': '#9966ff',
        'label': 'Холостой сброс (м\u00b3/с)',
    }
}


def plotter(
    data: Iterable, title: str, ylabel: str, lines: List[str]
) -> io.BytesIO:

    _, ax = plt.subplots(figsize=(6, 4))

    values = []
    dates = [i.date for i in data]
    for line in lines:
        values = [getattr(i, line) for i in data]
        plt.plot(dates, values, **PARAMS[line], lw=1)
        ax.fill_between(dates, values, 0, color=PARAMS[line]['color'], alpha=0.2)  # noqa(E501)

    ax.legend(labelcolor='#444444')
    ax.figure.autofmt_xdate()
    ax.tick_params(labelsize='small', labelcolor='#444444')
    ax.set_xlim(min(dates), max(dates))
    ax.set_ylim(min(values), max(values)) if len(lines) == 1 else ax.set_ylim(0)  # noqa(E501)

    plt.subplots_adjust(left=0.15)
    plt.ylabel(ylabel, color='#444444')
    plt.title(title)
    plt.grid(True)

    pic = io.BytesIO()
    plt.savefig(pic, format='png', dpi=200)
    plt.close()
    pic.seek(0)
    return pic


async def get_water_situations(
    reservoir: ReservoirModel, period: Tuple[dt.date]
) -> AsyncQueryWrapper:

    water_situations = await objects.execute(SituationModel.select(
        ).where(
            SituationModel.reservoir == reservoir
        ).where(
            SituationModel.date.between(min(period), max(period))
        ).order_by(
            SituationModel.date
        )
    )

    if len(water_situations) == 0:
        raise NoDataError('Нет данных за указанный период.')

    return water_situations


async def plot_graph(
    reservoir: ReservoirModel, command: str, period: Tuple[dt.date]
):
    """
    This function return a photo with a graph
    """
    match command:
        case 'level':
            lines = ['level']
        case 'flows':
            lines = ['inflow', 'outflow', 'spillway']
        case _:
            raise KeyError

    water_situations = await get_water_situations(reservoir, period)

    date1, date2 = water_situations[0].date, water_situations[-1].date

    title = (
        f'{reservoir.name} водохранилище\n'
        f'ФПУ={reservoir.force_level} м, '
        f'НПУ={reservoir.normal_level} м, '
        f'УМО={reservoir.dead_level} м'
    )
    caption = (
        f'График за период с {date1.strftime("%d.%m.%Y")} '
        f'по {date2.strftime("%d.%m.%Y")}'
    )
    return plotter(water_situations, title, Y_LABEL[command], lines), caption
