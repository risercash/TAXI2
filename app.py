from handlers import dp
from aiogram import executor
from loader import bot
from aiogram.types import BotCommand
from main_funcs import cookie_start_update, start_parsing, end_subscrible
import asyncio
import aioschedule

from config import ADMIN

command = [BotCommand("start", "Перезапуск бота"),
           BotCommand("help", "Помощь по боту"),
           BotCommand("count", "Подсчет пользователей бота"),
           BotCommand("stop", "адм. Остановить отчетность"),
           BotCommand("users", "адм. Список пользователей")
           ]


async def on_shutdown(dp):
    await bot.send_message(ADMIN, 'Бот экстренно закрылся!!!')
    await bot.close()


async def on_startup(dp):
    #await bot.send_message(ADMIN, 'Бот Перезапустился!!!')
    asyncio.create_task(cookie_start_update())
    #asyncio.create_task(scheduler())  # Запускаем планировщик
    asyncio.create_task(start_parsing())  # Запускаем парсер
    asyncio.create_task(end_subscrible())
    await bot.set_my_commands(command)


async def scheduler():
    """ ===== Так подключается планировщик ===== """
    aioschedule.every(12).hours.do(
        cookie_start_update)  # Каждые 12 часов обновляем cookies
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
