from datetime import datetime
from aiogram import types



def phone():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(
        text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(
        text="Отправить местоположение", request_location=True)
    return keyboard.add(button_phone, button_geo)


def subscribe(user, number):
    menu = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(
        text="Тест 12 часов", callback_data=f"day:0.5:{user.id}:{number}")
    menu.insert(button)
    button = types.InlineKeyboardButton(
        text="Тест 24 часа", callback_data=f"day:1:{user.id}:{number}")
    menu.insert(button)
    button = types.InlineKeyboardButton(
        text="Подписка 1 месяц", callback_data=f"day:30:{user.id}:{number}")
    menu.insert(button)
    button = types.InlineKeyboardButton(
        text="Вечный доступ", callback_data=f"day:10000:{user.id}:{number}")
    menu.insert(button)
    button = types.InlineKeyboardButton(
        text="Отказать", callback_data=f"devil:365:{user.id}:{number}")
    return menu.insert(button)


def die_sub(users, taxi_users):
    menu = types.InlineKeyboardMarkup(row_width=1)
    drivers = taxi_users.items()
    for key, value in drivers:
        if len(key) < 5:            
            continue
        if value[1] < datetime.now():
            continue
        for user in users:
            
            if user["user_id"] == value[0]:
                name = user["full_name"]
                subscr = user["subscribe"].strftime("%d.%m.%y %H:%M")
                break
        button = types.InlineKeyboardButton(
            text=f"{key}: {name} {subscr}", callback_data=f"die:{value[0]}:{key}")#  _, user_id, name, car_num
        menu.insert(button)
            
    return menu

def die_sub(users, taxi_users):
    menu = types.InlineKeyboardMarkup(row_width=1)
    drivers = taxi_users.items()
    for key, value in drivers:
        if len(key) < 5:            
            continue
        if value[1] < datetime.now():
            continue
        for user in users:
            
            if user["user_id"] == value[0]:
                name = user["full_name"]
                subscr = user["subscribe"].strftime("%d.%m.%y %H:%M")
                break
        button = types.InlineKeyboardButton(
            text=f"{key}: {name} {subscr}", callback_data=f"die:{value[0]}:{key}")#  _, user_id, name, car_num
        menu.insert(button)
            
    return menu