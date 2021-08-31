from aiogram.types import ReplyKeyboardMarkup

buttons = ["🚘 Сменить машину", "🚖 Я новый водитель"]


def start(adm=None):
    menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    menu.row("🚘 Сменить машину", "🚖 Я новый водитель")
    if adm:
        menu.row("☠️ За борт", "🤪 Подписчики")
    return menu