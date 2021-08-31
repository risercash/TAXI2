from aiogram.types.message import Message
from config import ADMIN, Taxi
import os
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from loader import bot, dp
import pickle
import asyncio
import time


def run_browser():
    """ ===== Запускаем браузер ===== """

    userAgent = 'Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/10.0 YaBrowser/20.3.2.277.11 Mobile/15E148 Safari/604.1'
    options = Options()

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size-minimize_window")
    options.add_argument(f"--user-agent={userAgent}")
    options.add_argument('--disable-infobars')
    options.add_experimental_option(
        "excludeSwitches", ["ignore-certificate-errors"])
    return webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def find_element(br, selector):
    return WebDriverWait(br, 6).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))


def check_exists_by_css(br, selector):
    try:
        br.find_element_by_xpath(selector)
    except NoSuchElementException:
        return False
    return True


def new_cookies(br):
    br.get("https://lk.taximeter.yandex.ru/report/company/")
    find_element(
        br, 'body > div > div.main > div.signin-card.signin-card-bg.clearfix > form > button:nth-child(2)').click()  # Кликаем
    pickle.dump(br.get_cookies(), open('cookies', 'wb'))


async def inter_taxi():
    br = run_browser()
    br.get("https://lk.taximeter.yandex.ru/report/company/")
    # Кликаем войти по паспорту
    find_element(
        br, 'body > div > div.main > div.signin-card.signin-card-bg.clearfix > form > div > a').click()

    try:
        # Вводим логин
        find_element(br, '#passp-field-login').send_keys('Lortindas@yandex.ru')
        find_element(br, '#passp\:sign-in').click()  # Кликаем далее
        await asyncio.sleep(1)
        # Вводим пароль
        find_element(br, '#passp-field-passwd').send_keys('rgI4TIFRZ')
    except:
        return False

    find_element(br, '#passp\:sign-in').click()  # Кликаем войти

    isexist = check_exists_by_css(
        br, '#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > div > div.auth-challenge__call > form > div.passp-button > button')
    if isexist == False:
        find_element(br, '#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div.passp-route-forward > div > div > div > div.auth-challenge__call > form > div.passp-button > button').click()  # Кликаем ввести код
        
        await bot.send_message(ADMIN, "⛔ SMS ⛔")
        
        while len(Taxi.sms) < 3:
            await asyncio.sleep(1)
        find_element(br, '#passp-field-phoneCode').send_keys(Taxi.sms)
        find_element(br, '#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.PagePopup > div:nth-child(3) > form > div:nth-child(2) > button').click()

    Taxi.sms = ""
    new_cookies(br)


async def rerun_browser():
    br = run_browser()
    br.get("https://lk.taximeter.yandex.ru/report/company/")
    for cookie in pickle.load(open('cookies', 'rb')):
        br.add_cookie(cookie)
    time.sleep(5)
    br.refresh()

    try:
        find_element(br, 'body > div.container-wrap > div.container.container-horizontal > div.hspan0 > div > div > div.vspan0.container-form > div > div > ul.toolbar > li:nth-child(2) > button > img').click()  # НА ПРИНТЕР
        find_element(br, 'body > div.container-wrap > div.container.container-horizontal > div.hspan0 > div > div > div.vspan0.container-form > div > div > ul.toolbar > li.open > ul > li:nth-child(2) > a').click()  # Кликаем
        pickle.dump(br.get_cookies(), open(
        'cookies', 'wb'))
    except:
        br.close()
        await inter_taxi()

    br.close()


def br_exception(br):
    br.refresh()
    # Кликаем войти по паспорту
    find_element(
        br, 'body > div > div.main > div.signin-card.signin-card-bg.clearfix > form > div > a').click()


def new_file(br):  # Эту функцию я вызываю для получения этого файла.
    br.refresh()
    find_element('body > div.container-wrap > div.container.container-horizontal > div.hspan0 > div > div > div.vspan0.container-form > div > div > ul.toolbar > li:nth-child(2) > button > img').click()
    find_element('body > div.container-wrap > div.container.container-horizontal > div.hspan0 > div > div > div.vspan0.container-form > div > div > ul.toolbar > li.open > ul > li:nth-child(2) > a').click()  # Кликаем