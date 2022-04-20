import logging

import os
import random

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command
from aiogram.types import BotCommand
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from dotenv import load_dotenv

from keyboards import category_choice_keyboard, choice_callback

from wisdoms import wisdoms

# configure logging
logging.basicConfig(
    format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG)

# load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# basic configurations for bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    Handler for /start command

    :param message:
    """
    await message.answer(f'Бот может подсказать тебе мудрость, '
                         f'столь необходимую в наше время. '
                         f'Введи команду /wisdom')


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    """
    Handler for /help command

    :param message:
    """
    text = [
        'Список команд: ',
        '/wisdom - получить мудрость'
    ]
    await message.answer(text='\n'.join(text))


@dp.message_handler(Command('wisdom', ignore_case=True))
async def bot_wisdom(message: types.Message):
    await message.answer(text=emojize(':crystal_ball: Выберите категорию:'),
                         reply_markup=category_choice_keyboard)


@dp.callback_query_handler(choice_callback.filter())
async def handle_wisdom(callback_query: types.CallbackQuery,
                        callback_data: dict):
    question = random.choice(wisdoms.get(callback_data.get('type')))
    await callback_query.message.delete()
    await callback_query.message.answer(
        text=emojize(f':woman_mage: {question} :woman_mage:'))


async def on_startup(dispatcher: Dispatcher):
    """
    Set up the bot commands

    :param dispatcher:
    """
    await dispatcher.bot.set_my_commands([
        BotCommand("start", "Запустить бота"),
        BotCommand("help", "Помощь"),
        BotCommand("wisdom", "Мудрость")
    ])


async def on_shutdown(dispatcher: Dispatcher):
    """
    Shut down the bot.

    :param dispatcher:
    """
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)
