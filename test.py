# from aiogram.utils import executor
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
#
# bot = Bot('5817733284:AAFimuh5uvyb6ygqlAdZgWMeBTXjliRSh2Y')
# dp = Dispatcher(bot)
#
# @dp.message_handler(commands=['start', 'help'])
# async def command_start(message: types.Message):
#     await message.reply('Здаров')
#
# @dp.message_handler(commands=['команда'])
# async def echo(message: types.Message):
#     await message.answer(message.text)
#
# @dp.message_handler(lambda message: 'такси' in message.text)
# async def taxi(message: types.Message):
#     await message.answer('такси')
#
#
# @dp.message_handler()
# async def empty(message: types.Message):
#     await message.answer('Нет такой команды')
#     await message.delete()
#
# executor.start_polling(dp, skip_updates=True)