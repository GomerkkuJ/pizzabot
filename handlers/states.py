# from aiogram.dispatcher.filters.state import State, StatesGroup
#
# # Процессы регистрации
# class Registration(StatesGroup):
#     getting_name_state = State()
#     getting_phone_number = State()
#     getting_location = State()
#
# # Процессы для Выбора опредленного товара
# class GetProduct(StatesGroup):
#     getting_pr_count = State()
#
# # Процессы при работе с корзиной
# class Cart(StatesGroup):
#     waiting_for_product = State()
#     waiting_new_count = State()
#
# # Процессы при оформелении заказа
# class Order(StatesGroup):
#     waiting_location = State()
#     waiting_pay_type = State()
#     waiting_accept = State()