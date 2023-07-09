import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.exceptions import NoDataError
from bot.markups import (command_buttons, get_markup_with_items,
                         get_markup_with_objs, main_cb, time_buttons)
from bot.utils import reservoir_info
from services.api_handlers import get_regions, get_reservoir, get_reservoirs


class MainState(StatesGroup):
    waiting_for_region = State()
    waiting_for_reservoir = State()
    waiting_for_command = State()
    waiting_for_period = State()
    waiting_for_date1 = State()
    waiting_for_date2 = State()


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'], state='*')
    dp.register_message_handler(menu, text=['Показать меню'], state='*')
    dp.register_message_handler(menu, commands=['menu'], state='*')
    dp.register_callback_query_handler(back, main_cb.filter(action='start'), state='*')  # noqa (E501)
    dp.register_callback_query_handler(
        info_command_handler,
        main_cb.filter(action='command'),
        main_cb.filter(answer='info'),
        state=MainState.waiting_for_command,
    )
    dp.register_callback_query_handler(
        plot_command_handler,
        main_cb.filter(action='command'),
        state=MainState.waiting_for_command,
    )
    dp.register_callback_query_handler(
        regions_handler,
        main_cb.filter(action='region'),
        state=[MainState.waiting_for_region, MainState.waiting_for_command],
    )
    dp.register_callback_query_handler(
        reservoirs_handler,
        main_cb.filter(action='reservoir'),
        state=[MainState.waiting_for_reservoir, MainState.waiting_for_period],
    )


async def start(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await state.finish()
    text = (
        'Привет! Я бот, который поможет тебе получить данные '
        'о гидрологической обстановке на водохранилищах ГЭС России. '
        'Чтобы начать, нажми *"Показать меню"*'
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Показать меню')
    await message.answer(
        text,
        reply_markup=markup,
        parse_mode='Markdown',
        disable_notification=True,
    )


async def menu(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends text "Показать меню"
    """
    await state.finish()
    regions = await get_regions()
    markup = get_markup_with_objs(action='region', objs=regions)
    await message.answer(
        text='Выберите регион:',
        reply_markup=markup,
        disable_notification=True,
        disable_web_page_preview=True,
    )
    await message.delete()
    await MainState.waiting_for_region.set()


async def back(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    """
    This handler will be called when the user sends
    query with "start" action
    """
    await state.finish()
    regions = await get_regions()
    markup = get_markup_with_objs(action='region', objs=regions)
    await query.message.edit_text(
        text='Выберите регион:', reply_markup=markup
    )
    await query.answer()
    await MainState.waiting_for_region.set()


async def regions_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    """
    This handler will be called when the user sends
    query with "region" action
    """
    await state.update_data(region=callback_data['answer'])
    reservoirs = await get_reservoirs(region=callback_data['answer'])
    markup = get_markup_with_objs(
        action='reservoir', objs=reservoirs, lookup='id')
    back_button = types.InlineKeyboardButton(
        'Назад', callback_data=main_cb.new(action='start', answer='_')
    )
    markup.add(back_button)
    await query.message.edit_text(
        'Выберите водохранилище:', reply_markup=markup
    )
    await query.answer()
    await MainState.waiting_for_reservoir.set()


async def reservoirs_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    """
    This handler will be called when the user sends
    query with "reservoir" action
    """
    await state.update_data(reservoir=callback_data['answer'])
    data = await state.get_data()
    markup = get_markup_with_items(action='command', items=command_buttons)
    back_button = types.InlineKeyboardButton(
        'Назад',
        callback_data=main_cb.new(action='region', answer=data['region']),
    )
    markup.add(back_button)
    await query.message.edit_text('Выберите команду:', reply_markup=markup)
    await query.answer()
    await MainState.waiting_for_command.set()


async def plot_command_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    """
    This handler will be called when the user sends
    query with "command" action
    """
    await state.update_data(command=callback_data['answer'])
    data = await state.get_data()

    markup = get_markup_with_items(action='period', items=time_buttons)
    back_button = types.InlineKeyboardButton(
        'Назад',
        callback_data=main_cb.new(
            action='reservoir', answer=data['reservoir']
        ),
    )
    markup.add(back_button)

    await query.message.edit_text('Выберите период:', reply_markup=markup)
    await query.answer()
    await MainState.waiting_for_period.set()


async def info_command_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    """
    This handler will be called when the user sends
    query with "command" action and "info" answer
    """
    data = await state.get_data()

    try:
        reservoir = await get_reservoir(id=data['reservoir'])
        await query.message.edit_text(
            reservoir_info(reservoir), parse_mode='Markdown'
        )
    except (KeyError, TypeError, NoDataError) as error:
        logging.error(repr(error))
        await query.message.edit_text('Упс.. что-то пошло не так.')

    await query.answer()
    await state.finish()
