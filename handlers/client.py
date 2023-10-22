from aiogram import types, Dispatcher
from create_bot import dp, bot, MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_kb
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext


class Registration(StatesGroup):
    getting_name_state = State()
    getting_phone_number = State()
    getting_location = State()


class GetProduct(StatesGroup):
    getting_pr_count = State()


class Cart(StatesGroup):
    waiting_for_product = State()
    waiting_new_count = State()


class Order(StatesGroup):
    waiting_location = State()
    waiting_pay_type = State()
    waiting_accept = State()


@dp.message_handler(commands=['start', 'help'], state="*")
async def command_start(message: types.Message):
    if message.chat.type == "group":
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttp://t.me/Pizza_SheefGGbot')
    else:
        await bot.send_message(message.from_user.id, 'Приятного аппетита')  # reply_markup=kb_client)
        await message.delete()

        user_id = message.from_user.id
        checker = sqlite_db.check_user(user_id)
        if checker:
            await message.answer('Выбери продукт', reply_markup=client_kb.products_kb())

        else:
            await message.answer('Привет, самая лучшая пицца Бот\nОтправь имя для регистрации')
            await Registration.getting_name_state.set()


@dp.message_handler(state=Registration.getting_name_state)
async def get_name(message: types.Message, state: FSMContext):
    user_answer = message.text
    await state.update_data(name=user_answer)
    await message.answer('Имя сохранил\nОтправь номер телефона', reply_markup=client_kb.phone_number_kb())
    await Registration.getting_phone_number.set()


@dp.message_handler(state=Registration.getting_phone_number, content_types=['contact'])
async def get_number(message: types.Message, state: FSMContext):
    user_answer = message.contact.phone_number
    await state.update_data(number=user_answer)

    await message.answer('Номер сохранил\n', reply_markup=client_kb.location_kb())
    # await Registration.getting_location.set()
    # await state.finish()

# @dp.message_handler(state=Registration.getting_location, content_types=['location'])
# async def get_location(message: types.Message, state: FSMContext):
#     user_answer = message.location.latitude
#     user_answer_2 = message.location.longitude
#
#     await state.update_data(latitude=user_answer, longitude=user_answer_2)

    # await message.answer('Локацию сохранил')
    all_info = await state.get_data()
    name = all_info.get('name')
    phone_number = all_info.get('number')
    # latitude = all_info.get('latitude')
    # longitude = all_info.get('longitude')
    user_id = message.from_user.id

    sqlite_db.add_user(user_id, name, phone_number) #latitude, longitude)
    print(sqlite_db.get_users())
    await message.answer('Выберите продукт из списка', reply_markup=client_kb.products_kb())
    await state.finish()


# @dp.message_handler(content_types=['text'])
async def text_messages(message: types.Message, state: FSMContext):
    user_answer = message.text

    # Актуальный список продуктов
    actual_products = [i[0] for i in sqlite_db.get_names_from_menu()]

    if user_answer == 'Корзина':
        user_cart = sqlite_db.get_user_cart(message.from_user.id)

        if user_cart:
            result_answer = 'Ваша корзина:\n'

            for i in user_cart:
                result_answer += f'Продукт: {i[1]}: {i[-1]} шт\n'

            await message.answer(result_answer, reply_markup=client_kb.cart_kb())

            await Cart.waiting_for_product.set()

        else:
            await message.answer('Ваша корзина пустая')

    elif user_answer == 'Оформить заказ':
        await message.answer('Оформляем заказ')

    elif user_answer in actual_products:
        product = sqlite_db.get_product_from_menu(name=message.text)

        await message.answer('Выберите количество', reply_markup=client_kb.product_count())
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=product[0],
            caption=f"<b>Наименование:</b> {product[1]}\n"
                    f"Описание: {product[2]}\n"
                    f"<i>Цена: {product[3]}</i>",
        )

        await state.update_data(user_product=message.text)
        await GetProduct.getting_pr_count.set()


@dp.message_handler(state=GetProduct.getting_pr_count)
async def get_pr_count(message: types.Message, state: FSMContext):
    product_count = message.text

    user_data = await state.get_data()
    user_product = user_data.get('user_product')
    try:
        sqlite_db.add_product_to_cart(message.from_user.id, user_product, int(product_count))
        await message.answer('Продукт добавлен\nеще?', reply_markup=client_kb.products_kb())
    except ValueError:
        await message.answer('Выберите продукт из списка', reply_markup=client_kb.products_kb())
    await state.finish()


# Обработчик действий в корзине
@dp.message_handler(state=Cart.waiting_for_product)
async def cart_function(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Очистить':
        sqlite_db.delete_from_cart(user_id)
        await message.answer('Корзина очищена')
    elif user_answer == 'Оформить заказ':
        user_cart = sqlite_db.get_user_cart(message.from_user.id)
        if user_cart:
            result_answer = 'Ваш заказ:\n'
            admin_message = 'Новый заказ:\n'
            for i in user_cart:
                result_answer += f'Продукт: {i[1]}: {i[-1]} шт\n'
                admin_message += f'Продукт: {i[1]}: {i[-1]} шт\n'
            await message.answer(result_answer, reply_markup=client_kb.products_kb())
            sqlite_db.delete_from_cart(user_id=message.from_user.id)
            await message.answer('Успешно оформлен, отправьте локацию', reply_markup=client_kb.location_kb())
            await state.finish()
    if message.text == "Назад":
        await message.answer('Выберите продукт из списка', reply_markup=client_kb.products_kb())
        await state.reset_state(with_data=False)


@dp.message_handler(content_types=['location'])
async def get_location(message: types.Message, state: FSMContext):
    user_answer = message.location.latitude
    user_answer_2 = message.location.longitude
    await state.update_data(latitude=user_answer, longitude=user_answer_2)
    await message.answer('Локацию сохранил\nВашь заказ в обработке')
    all_info = await state.get_data()
    latitude = all_info.get('latitude')
    longitude = all_info.get('longitude')
    await message.answer('Хотите сделать еще заказ?', reply_markup=client_kb.products_kb())
    await state.finish()

    # await bot.send_message(860227652, admin_message)
    # sqlite_db.delete_from_cart(user_id)


# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт 9:00 до 20:00, Пт-Сб 10:00 до 23:00')


# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Город Ташкент')  # reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    # dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(text_messages, content_types="text")
    dp.register_message_handler(pizza_open_command, text=["Режим_работы"])
    dp.register_message_handler(pizza_place_command, text=['Расположение'])
    dp.register_message_handler(pizza_menu_command, text='Меню')
