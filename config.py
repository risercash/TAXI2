import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Yakassabot
URL = os.getenv("URL")  # for pymongo
ADMIN = os.getenv("ADMIN")
ME = os.getenv("ME")
ASM = os.getenv("ASM")

class Taxi:
    work = True
    users = {}
    sms = ""