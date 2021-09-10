import asyncio
import os
from datetime import datetime

from loguru import logger

from config import ADMIN, ME, ASM, Taxi
from loader import bot
from web.myweb import Web
from web.web import rerun_browser


web = Web()


async def start_parsing():
    await bot.send_message(ME, 'Включил бота!')

    web.initial_database()

    while True:
        await asyncio.sleep(1)
        if not os.path.exists('report.html'):
            web.initial_database()

        #rows = web.get_new_rows_in_database()
        try:
            rows = web.get_new_rows_in_database()
        except Exception as err:
            logger.error(err)
            await rerun_browser()
            web.initial_database()
            continue
 
        if type(rows) == bool:
            logger.error("bool")
            continue

        for row in rows:
            if row[0]=='Number':
                #rows.remove(row)
                continue
            logger.debug(row)

            ans = f'<i>Куда:</i> {row[8]}\n<i>Откуда:</i> {row[7]}\n\n{row[14]}\n\n🎫 {row[0]}\n📑 {row[1]} 🕕 {row[2]}\n\n🚖 <code>{row[9]}</code> {row[12]}\n👨 ({row[10]}) {row[11]}\n'
            car_number = row[9]
            drivers = list(Taxi.users.keys())
            if car_number in drivers:
                try:
                    await bot.send_message(Taxi.users[row[9]][0], ans)
                except: pass
                
            if Taxi.work == True:
                await bot.send_message(ADMIN, ans)
                await bot.send_message(ME, ans)


async def cookie_start_update():
    while True:
        await rerun_browser()
        web.update_cookies()
        await asyncio.sleep(24000)


async def end_subscrible():
    while True:
        for user, value in Taxi.users.items():
            if value[1] < datetime.now():
                Taxi.users.pop(user)
        await asyncio.sleep(1800)
