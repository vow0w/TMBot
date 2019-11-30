import bs4 as bs4
import requests
import datetime
from subprocess import call
import test

dz = ['', '']
change = ['', '']

URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"
KEY = "trnsl.1.1.20191110T092011Z.7d18b9f5db697192.14ff5339104675dd87ad652a5fd794605e0fb4d2"

def checkWeek():
    call(["node", "chet.js"])
    week = 12
    # 0 - под, 1 - над
    with open("week.txt") as f:
        week = f.read()
    if (datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6):
        if week == "0":
            return f"Неделя над чертой"
        else:
            return "Неделя под чертой"
    elif (datetime.datetime.today().weekday() != 5 or datetime.datetime.today().weekday() != 6):
        if week == "0":
            return f"Неделя под чертой"
        else:
            return f"Неделя над чертой"

def getWeek():
    with open("week.txt") as f:
        week = f.read()
    return week

def translateMe(name):
    params = {
        'key': KEY,
        'text': name,
        'lang': "en-ru"
    }
    response = requests.get(URL, params=params);
    return response.json()['text'][0]

class VkBot:
    def __init__(self, user_id):
        print("\nСоздан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ["ПРИВЕТ", "РАСПИСАНИЕ", "КОМАНДЫ", "ПОМОЩЬ", "ПОКА", "ДЗ", "ЗАМЕНЫ", "ACLEAR", "НЕДЕЛЯ", "СПИСОК"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")
        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        name = user_name.split()[0]
        name = translateMe(name)
        return name

    def new_message(self, message):

        date = datetime.date

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Добрый день, студент группы 18-4ТМ, {self._USERNAME}!"

        # Расписание
        if message.upper() == self._COMMANDS[1]:
            if date.today().weekday() == 0:
                return checkWeek() + f"\nРасписание на Вторник:\n2) История\n3) Техническая механика\n4) Математика"
            if date.today().weekday() == 1:
                return checkWeek() + f"\nРасписание на Среду:\n1) Электротехника и электроника\n2) Процессы формоогбразования и инструменты\n3) МДК.04.01(над) или Материаловедение(под)"
            if date.today().weekday() == 2:
                return checkWeek() + f"\nРасписание на Четвер:\n1) Иностранный язык\n2) МДК.04.01\n3) Физическая культура"
            if date.today().weekday() == 3:
                return checkWeek() + f"\nРасписание на Пятницу:\n1) Математика\n2) Процессы формообразования и инструменты\n3) Техническая механика(над) или История(под)"
            if date.today().weekday() == 4:
                return checkWeek() + f"\nРасписание на Субботу:\n1) Материаловедение\n2) Инженерная графика\n3) Инженерная графика"
            if date.today().weekday() == 5:
                return checkWeek() + f"\nРасписание на Понедельник:\n1) Электротехника и электроника\n2) Материаловедение\n3) Бережливое производство"
            if date.today().weekday() == 6:
                return checkWeek() + f"\nРасписание на Понедельник:\n1) Электротехника и электроника\n2) Материаловедение\n3) Бережливое производство"
            return

        # Команды
        elif message.upper() == self._COMMANDS[2]:
            return f"Весь список команд:\n1) Привет - приветсвие с ботом.\n2) Расписание - показывает расписание на следующий день.\n3) Дз - показывает домашнее задание на следующий день.\n4) Замены - показывает замены на следующий день.\n5) Пока - прощание с ботом."

        # Помощь
        elif message.upper() == self._COMMANDS[3]:
            return f"Весь список команд:\n1) Привет - приветсвие с ботом.\n2) Расписание - показывает расписание на следующий день.\n3) Дз - показывает домашнее задание на следующий день.\n4) Замены - показывает замены на следующий день.\n5) Пока - прощание с ботом."

        # Пока
        elif message.upper() == self._COMMANDS[4]:
            return f"Пока, {self._USERNAME}!"

        # Дз
        if message.upper().find(self._COMMANDS[5], 0) != -1:
            arg = message.upper().replace(self._COMMANDS[5] + " ", "")
            if (arg != "" and arg != "ДЗ"):
                dz[0] = arg.lower().replace(',', '\n')
                dz[1] = self._USERNAME
                return f"ДЗ на завтра:\n" + dz[0] + "\nДобавил: " + dz[1]
            elif (arg == "ДЗ" or arg == "") and dz[0] != '':
                return f"ДЗ на завтра:\n" + dz[0] + "\nДобавил: " + dz[1]
            else:
                return f"На завтра нет дз"


        # Замены
        if message.upper().find(self._COMMANDS[6], 0) != -1:
            arg = message.upper().replace(self._COMMANDS[6] + " ", "")
            if (arg != "" and arg != "ЗАМЕНЫ"):
                change[0] = arg.lower().replace(',', '\n')
                change[1] = self._USERNAME
                return f"Замены на завтра:\n" + change[0] + "\nДобавил: " + change[1]
            elif (arg == "ЗАМЕНЫ" or arg == "") and change[0] != '':
                return f"Замены на завтра:\n" + change[0] + "\nДобавил: " + change[1]
            else:
                return f"На завтра нет замен"

        # aclear
        if message.upper() == self._COMMANDS[7]:
            dz[0] = ''; change[0] = '';
            dz[1] = ''; change[1] = '';
            return f"Списки были очищены!"

        # неделя
        if message.upper() == self._COMMANDS[8]:
            return getWeek()

        # список
        if message.upper().find(self._COMMANDS[9], 0) != -1:
            arg = message.upper().replace(self._COMMANDS[9] + " ", "")
            if (arg != "" and arg != "список"):
                return test.animelist(arg.lower().replace(',', '\n'))

        else:
            return "Я не знаю такую команду!"


    @staticmethod
    def _clean_all_tag_from_str(string_line):
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        return result