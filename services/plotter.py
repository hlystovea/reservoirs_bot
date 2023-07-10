import datetime as dt
import io
from typing import Iterable

import matplotlib.pyplot as plt

from bot.exceptions import NoDataError
from services.api_handlers import get_situations
from services.schemas import Reservoir


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
    data: Iterable, title: str, ylabel: str, lines: list[str]
) -> io.BytesIO:

    fig, ax = plt.subplots(figsize=(6, 4))
    fig.subplots_adjust(left=0.15)
    fig.suptitle(title.split('\n')[0], x=0.525)

    values = []
    dates = [i.date for i in data]
    for line in lines:
        values = [getattr(i, line) for i in data]
        ax.plot(dates, values, **PARAMS[line], lw=1)
        ax.fill_between(dates, values, 0, color=PARAMS[line]['color'], alpha=0.2)  # noqa(E501)

    ax.figure.autofmt_xdate()
    ax.tick_params(labelsize='small', labelcolor='#444444')
    ax.set_xlim(min(dates), max(dates))
    ax.set_ylim(min(values), max(values)) if len(lines) == 1 else ax.set_ylim(0)  # noqa(E501)

    ax.legend(labelcolor='#444444')
    ax.set_ylabel(ylabel, color='#444444')
    ax.set_title(title.split('\n')[-1], size='small', color='#444444')
    ax.grid(True)

    pic = io.BytesIO()
    plt.savefig(pic, format='png', dpi=200)
    plt.close()
    pic.seek(0)
    return pic


async def plot_graph(
    reservoir: Reservoir, command: str, period: tuple[dt.date]
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

    water_situations = await get_situations(
        reservoir_id=reservoir.id,
        start=min(period),
        end=max(period))

    if len(water_situations) == 0:
        raise NoDataError('Нет данных за указанный период.')

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
