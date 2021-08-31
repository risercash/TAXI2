import asyncio
from asyncio.tasks import create_task
from sys import hash_info
from loguru import logger
import tobase
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message, user
from config import ADMIN, ME
from keyboards.default import menu
from keyboards.inline import buttons as btn
from loader import bot, dp
from web.myweb import Web
from tobase import Taxi
from datetime import datetime
from datetime import timedelta


web = Web()


async def first_message(message):
    """ ===== Эта функция для вывода первого сообщения ===== """
    user = message.from_user
    if user.id in [int(ADMIN), int(ME)]:
        adm = True
    else:
        adm = None
    # Сюда вставляется ссылка на картинку
    file = 'https://i.postimg.cc/8PnDLCC0/e04fac51ca815233fd07043583.jpg'
    await message.answer_photo(file,
                               caption=f'''
    <b>     Привет {user.full_name}!</b>

    ''', reply_markup=menu.start(adm))


@dp.message_handler(CommandStart())
async def show_menu(message: Message):
    await first_message(message)
    new_user = tobase.new_user(usr=message.from_user)
    if new_user:
        if message.from_user.username:
            await bot.send_message(ADMIN, f'Новый пользователь: @{message.from_user.username}({message.from_user.id}) {message.from_user.first_name}')
        else:
            await bot.send_message(ADMIN, f'Новый пользователь: ({message.from_user.id}) {message.from_user.first_name}')
    if message.from_user.id == int(ADMIN):
        await message.answer('Уведомления включил')
        Taxi.work == True


@dp.message_handler(Command("stop"))
async def deep_cert(message: Message):
    if message.from_user.id == int(ADMIN):
        await message.answer('*** Уведомления отключены!!! ***')
        Taxi.work == False


@dp.message_handler(Text("🚘 Сменить машину"))
@dp.message_handler(Text("🚘 Сменить машину"), state="*")
async def deep_cert(message: Message, state: FSMContext):
    driver = await tobase.find_driver(message.from_user.id)
    if len(driver["car_number"]) < 5:
        await message.answer("У нас не зарегистрирован Ваш автомобиль!\n Нажмите '🚖 Я новый водитель'")
        return
    await message.answer("Введите номер вашего автомобиля на русском языке")
    await state.set_state("newnum")


@dp.message_handler(state="newnum")
async def phone_number(message: Message, state: FSMContext):
    if message.text in menu.buttons or len(message.text) > 10 or len(message.text) < 7:
        await message.answer("Неправильно ❗\nВведите номер вашего автомобиля на русском языке")
        return

    usr = message.from_user
    number = message.text.upper()
    photo = await bot.get_user_profile_photos(user_id=usr.id)
    text = f'🆔: {usr.id}\n👨🏻‍🦰: {usr.first_name} {usr.last_name}\n🤖: {usr.username}\n🚖: {number}'
    try:
        await bot.send_photo(ADMIN, photo=photo.photos[0][0].file_id, caption=text)
    except:
        await bot.send_message(ADMIN, text)
    logger.info(number)
    await message.answer("Хорошо. Номер принят.")
    await tobase.update_car_number(usr.id, number)
    await tobase.change_car_number()
    await state.reset_state()


@dp.message_handler(Text("🚖 Я новый водитель"))
async def deep_cert(message: Message, state: FSMContext):
    # , reply_markup=btn.phone())
    await message.answer("Введите ваш номер телефона в формате 7...")
    await state.set_state("number")


@dp.message_handler(state="number")
async def phone_number(message: Message, state: FSMContext):
    num = message.text
    mylen = len(num)
    if num in menu.buttons or mylen != 11 or not num.isdigit():
        await message.answer("Неправильно ❗\nВведите ваш номер телефона в формате 7...")
        return
    if num == '79607071046':
        await message.answer("Это мой номер❗ Свои цифры надо присылать")
        return

    await message.answer("Введите номер вашего автомобиля на русском языке")
    await tobase.update_user_number(message.from_user.id, int(num))
    await state.update_data(phone_number=num)
    await state.set_state("car_number")


@dp.message_handler(state="car_number")
async def car_number(message: Message, state: FSMContext):
    if message.text in menu.buttons or len(message.text) > 10 or len(message.text) < 7:
        await message.answer("Неправильно ❗\nВведите номер вашего автомобиля на русском языке (ОБРАЗЕЦ)")
        return
    if message.text == 'М777ОН777':
        await message.answer("Это мой номер❗ Свои цифры надо присылать")
        return

    data = await state.get_data()
    phone = data['phone_number']
    usr = message.from_user
    car_number = message.text.upper()
    photo = await bot.get_user_profile_photos(user_id=usr.id)
    text = f'🆔: {usr.id}\n👨🏻‍🦰: {usr.first_name} {usr.last_name}\n🤖: {usr.username}\n📱: {phone}\n🚖: {car_number}'
    try:
        await bot.send_photo(ADMIN, photo=photo.photos[0][-1].file_id, caption=text, reply_markup=btn.subscribe(usr, car_number))
        await bot.send_photo(ME, photo=photo.photos[0][-1].file_id, caption=text, reply_markup=btn.subscribe(usr, car_number))
    except:
        await bot.send_message(ADMIN, text, reply_markup=btn.subscribe(usr, car_number))
        await bot.send_message(ME, text, reply_markup=btn.subscribe(usr, car_number))
    logger.info(car_number)
    await tobase.update_car_number(usr.id, car_number)
    await message.answer("Хорошо. Номер принят. Ожидайте..")
    await state.reset_state()


@dp.callback_query_handler(text_contains="day", state="*")
@dp.callback_query_handler(text_contains="day")
async def day(call: CallbackQuery):
    _, days, user_id, number = call.data.split(":")
    await call.answer(f'{number} одобрен на {days} дня(ей)', cache_time=60)
    if days == '0.5':
        subscribe = datetime.now() + timedelta(hours=12)
    else:
        subscribe = datetime.now() + timedelta(days=int(days))
    subscr = subscribe.strftime("%d.%m.%y %H:%M")
    Taxi.users[number] = (int(user_id), subscribe)
    await bot.send_message(user_id, f'Подписка одобрена!\n🆔: {user_id}\n🚖: {number}\n🕒: {subscr}')
    logger.info(f"{days=}, {user_id=}, {number=}, {subscr=}")
    await tobase.update_user_subscr(user_id, subscribe, number)


@dp.callback_query_handler(text_contains="devil")
async def day(call: CallbackQuery):
    _, days, user_id, number = call.data.split(":")
    await call.answer(f'{user_id} Отказали в подписке', cache_time=60)


@dp.message_handler(Text("☠️ За борт"))
async def die_subscr(message: Message, state: FSMContext):
    users = await tobase.show_users()
    menu = await die_sub(users, Taxi.users)
    await message.answer(f"{menu}\nУ кого уберем подписку?\nПришлите номер ID")
    await state.set_state("die")


@dp.message_handler(Text("🤪 Подписчики"))
async def die_subscr(message: Message, state: FSMContext):
    users = await tobase.show_users()
    await message.answer(await die_sub(users, Taxi.users))


@dp.message_handler(state="die")
async def die_hard(message: Message, state: FSMContext):
    if message.text == '0':
        await message.answer("Отменил ❗❗❗")
        await state.reset_state()
        return

    if not message.text.isdigit():
        await message.answer("Неправильно ❗\nВведите номер ID\nИли пришлите 0 для отмены")
        return

    await state.reset_state()
    user_id = int(message.text)
    await tobase.die_subscr(int(user_id))

    for key, value in Taxi.users.items():
        if value[0] == user_id:
            Taxi.users.pop(key)
            await message.answer(f'{user_id} Исключён')
            return
    await message.answer("Не нашел такого")


async def die_sub(users, taxi_users):

    menu = ''
    for key, value in taxi_users.items():
        if len(key) < 5:
            continue
        if value[1] < datetime.now():
            continue
        for user in users:

            if user["user_id"] == value[0]:
                name = user["full_name"]
                subscr = user["subscribe"].strftime("%d.%m.%y %H:%M")
                # _, user_id, name, car_num
                text = f"{value[0]}  {key}: {name} {subscr}\n"
                menu += text
                break
    return menu
