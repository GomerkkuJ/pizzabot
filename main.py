from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from data_base import sqlite_db

async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()


admin.register_handler_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)



executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
