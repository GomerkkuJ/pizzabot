from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types


bot = Bot('5817733284:AAFimuh5uvyb6ygqlAdZgWMeBTXjliRSh2Y', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
