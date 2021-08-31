import asyncio
from loguru import logger
import tobase
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message
from config import ADMIN, ME
from keyboards.default import menu
from keyboards.inline import buttons as btn
from loader import bot, dp
import pandas as pd
from config import Taxi



@dp.message_handler(Command("users"))
async def users(message: Message):
    users = await tobase.show_users()
    df = pd.DataFrame(users)
    df.to_excel('users.xlsx')
    with open('users.xlsx', 'rb') as file:
        await message.answer_document(file)


@dp.message_handler(Command("count"))
async def send(message: Message):
    count = len(await tobase.show_users())
    await message.answer(count)


@dp.message_handler(content_types=['text'])
async def sms(message: Message):
    if not message.text.isdigit() and len(message.text) !=4:
        return
    Taxi.sms = message.text