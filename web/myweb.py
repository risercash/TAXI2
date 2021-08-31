import requests
import pandas as pd
from loguru import logger
from datetime import datetime
import pickle


class Web(object):

    def __init__(self):
        self.cookies_list = []
        self.cookies_dict = {}
        self.update_cookies()

    def update_cookies(self):
        with open("cookies", 'rb') as cookies_file:
            self.cookies_list = pickle.load(cookies_file)
            for cookie in self.cookies_list:
                self.cookies_dict[cookie['name']] = cookie['value']
            self.cookies_dict = dict(self.cookies_dict)

    def get_url(self):
        now = datetime.today()
        date = now.strftime("%Y-%m-%d")
        hour = now.strftime("%H")
        return f'https://lk.taximeter.yandex.ru/report/items/company?datefield=0&status=0&time=true&discount=false&q=&payment&s={date}T{hour}%3A00&e={date}T{hour}%3A59&excel=true'

    def get_dataframe_from_html(self):
        tables = pd.read_html('report.html')
        return tables[0]

    def initial_database(self):  # load_initial_database()

        url = self.get_url()

        try:
            resp_text = requests.get(url, cookies=self.cookies_dict).text
        except:
            logger.error("requests.get error")
            return False

        with open('report.html', 'w', encoding='utf-8') as file:
            file.write(resp_text)
        return True

    def get_new_rows_in_database(self):
        """ Напиши мне в телеграм https://t.me/cashriser """
        prevDF = self.get_dataframe_from_html()

        url = self.get_url()

        try:
            resp_text = requests.get(url, cookies=self.cookies_dict).text

            with open('report.html', 'w', encoding='utf-8') as file:
                file.write(resp_text)

            newDF = self.get_dataframe_from_html()

            diffDF = newDF[~newDF['Number'].isin(prevDF['Number'][3:])]

            DFlist = []
            DFiter = diffDF.iterrows()
            cnt = 0
            for row in DFiter:
                if cnt > 1:
                    DFlist.append([])
                    for values in row[1]:
                        DFlist[cnt-2].append(values)
                cnt += 1
            return DFlist
        except:
            return False