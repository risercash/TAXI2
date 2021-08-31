import asyncio
import re
import pymongo

from datetime import datetime
from config import URL, Taxi
import ssl


col = pymongo.MongoClient(URL)
client = pymongo.MongoClient(URL, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
Users = client['TAXI']['Users']


def new_user(usr):
    ''' ==== База пользователей ==== '''
    new_user = Users.find_one({'user_id': usr.id})

    if not new_user:
        new_user = ({
            "user_id": usr.id,
            "username": usr.username,
            "full_name": usr.full_name,
            "number": "",
            "car_number": "-",
            "subscribe": datetime.now(),
            "date": datetime.today().strftime("%d.%m.%y %H:%M"),

        })
        Users.insert_one(new_user)
        return new_user


async def show_users(): return list(Users.find({}, {'_id': 0}))


async def update_user_number(user_id, number):
    Users.update_one({"user_id": user_id}, {'$set': {"number": number}})


async def update_car_number(user_id, car_number):
    Users.update_one({"user_id": int(user_id)}, {
                     '$set': {"car_number": car_number}})


async def update_user_subscr(user_id, subscr, car_number):
    Users.update_one({"user_id": int(user_id)}, {
                     '$set': {'car_number': car_number, "subscribe": subscr}})


async def die_subscr(user_id):
    Users.update_one({"user_id": int(user_id)}, {
                     '$set': {"subscribe": datetime.now()}})


async def change_car_number():
    for user in Users.find({}, {'_id': 0}):
        now = datetime.now()
        if now < user['subscribe']:
            Taxi.users[user['car_number']] = (user['user_id'], user['subscribe'])


async def find_driver(user_id): return Users.find_one({"user_id": user_id})


for user in Users.find({}, {'_id': 0}):
    now = datetime.now()
    if now < user['subscribe']:
        Taxi.users[user['car_number']] = (user['user_id'], user['subscribe'])
