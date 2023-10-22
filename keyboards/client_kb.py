from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base import sqlite_db
b1 = KeyboardButton('Режим_работы')
b2 = KeyboardButton('Расположение')
b3 = KeyboardButton('Меню')
# b4 = KeyboardButton('Поделится номером', request_contact=True)
# b5 = KeyboardButton('Отправить где я', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1).add(b2).add(b3)#.row(b4, b5)

# Кнопка для отправки номера телефона
def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Поделится контактом', request_contact=True)
    kb.add(button)
    return kb

def location_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Поделится локацией', request_location=True)
    kb.add(button)
    return kb

def product_count():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [KeyboardButton(str(i)) for i in range(1,10)]
    back = KeyboardButton('Назад')
    kb.add(*buttons, back)
    return kb


def cart_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Очистить')
    button2 = KeyboardButton('Оформить заказ')
    # button3 = KeyboardButton('Редактировать')
    button4 = KeyboardButton('Назад')

    kb.add(button, button2, button4)
    return kb


def pay_type_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Наличные')
    button2 = KeyboardButton('Картой')
    button3 = KeyboardButton('Назад')
    kb.add(button, button2, button3)
    return kb


def confirmation_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Подвердить')
    button2 = KeyboardButton('Отменить')
    button3 = KeyboardButton('Назад')
    kb.add(button, button2, button3)
    return kb

def products_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cart = KeyboardButton('Корзина')
    # of = KeyboardButton('Оформить заказ')
    all_products = sqlite_db.get_names_from_menu()
    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(cart)#of)
    kb.add(*buttons)
    return kb