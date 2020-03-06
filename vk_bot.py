import bs4 as bs4
from bs4 import BeautifulSoup
import requests
import datetime
import json

def writedz(dzinfo):
    with open('dz.json', 'w') as file_write:
        dz = {
            "dz" : dzinfo,
        }
        json.dump(dz, file_write)

def writechange(changeinfo):
    with open('change.json', 'w') as file_write:
        change = {
            "change" : changeinfo
        }
        json.dump(change, file_write)

def readdz():
    with open('dz.json', 'r') as file_read:
        load = str(json.load(file_read))
        dz = load.replace('{\'dz\': \'', '')
        dz2 = dz.replace('\'}', '')
        return dz2

def readchange():
    with open('change.json', 'r') as file_read:
        load = str(json.load(file_read))
        change = load.replace('{\'change\': \'', '')
        change2 = change.replace('\'}', '')
        return change2

def clearjsondz():
    with open('dz.json', 'w') as deldata:
        dz = {
            'dz': ''
        }
        json.dump(dz, deldata)

def clearjsonchange():
    with open('change.json', 'w') as deldata:
        dz = {
            'change': ''
        }
        json.dump(dz, deldata)

def checkweek():
    sessions = requests.Session()
    requestt = sessions.get('https://xn--d1ababprchchy.xn--p1ai/')
    if requestt.status_code == 200:
        soupp = BeautifulSoup(requestt.content, 'html.parser')
        divss = soupp.findAll('div', attrs={'id': 'body-inner'})
        for div in divss:
            titlee = div.find('span', attrs={'id': 'ugenr'}).text
            resultt = titlee.replace('Неделя', '')

    num = int(resultt)
    if (num % 2) == 0:
        if (datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6):
            return f"Неделя под чертой"
        return f"Неделя над чертой"
    else:
        if (datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6):
            return f"Неделя над чертой"
        return f"Неделя под чертой"

def weekday():
    sessions = requests.Session()
    requestt = sessions.get('https://xn--d1ababprchchy.xn--p1ai/')
    if requestt.status_code == 200:
        soupp = BeautifulSoup(requestt.content, 'html.parser')
        divss = soupp.findAll('div', attrs={'id': 'body-inner'})
        for div in divss:
            titlee = div.find('span', attrs={'id': 'ugenr'}).text
            resultt = titlee.replace('Неделя', '')

    num = int(resultt)
    if (num % 2) == 0:
        return "Неделя под чертой"
    else:
        return "Неделя над чертой"

def animelist(username):
    session = requests.Session()
    request = session.get('https://jut.su/user/'+str(username)+'/anime', headers={'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'})
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        divs = soup.findAll("div", class_="all_anime")
        Str = ""
        z = 1
        for div in divs:
            title = div.find('div', class_='aaname').text
            err = div.find('span', class_='av_active')
            if err == None:
                return f"Такого имя пользователся не сущеуствует"
            if err != None:
                starr = div.find('span', class_='av_active').text
            while z < 31:
                Str += "\n" + str(z) + ") " + title + " (" + starr + ")"
                z = z + 1
                break
        return f"Список просмотренных аниме пользователем " + username + f":" + Str

def translateMe(name):
    params = {
        'key': 'trnsl.1.1.20191110T092011Z.7d18b9f5db697192.14ff5339104675dd87ad652a5fd794605e0fb4d2',
        'text': name,
        'lang': "en-ru"
    }
    response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=params);
    return response.json()['text'][0]

class VkBot:
    def __init__(self, user_id):
        print("\nСоздан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ["ПРИВЕТ", "РАСПИСАНИЕ", "КОМАНДЫ", "ПОМОЩЬ", "ПОКА", "АНИМЕ", "СПИСОК", "ПРЕПОД", "ACLEARDZ", "ACLEARCHANGE", "ДЗ", "ЗАМЕНЫ"]

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
                return checkweek() + f"\nРасписание на Понедельник:\n1) Русский язык и культура речи(над) или МДК.04.01(под)\n2) Метрология\n3) Процессы формообразования и инструменты" + f"\n\n" + checkweek() + f"\nРасписание на Вторник:\n1) Информатика\n2) Техническая механика\n3) Бережливое производство"
            if date.today().weekday() == 1:
                return checkweek() + f"\nРасписание на Вторник:\n1) Информатика\n2) Техническая механика\n3) Бережливое производство" + f"\n\n" + checkweek() + f"\nРасписание на Среду:\n1) Электротехника и электроника\n2) Метрология\n3) Процессы формообразования и инструменты"
            if date.today().weekday() == 2:
                return checkweek() + f"\nРасписание на Среду:\n1) Электротехника и электроника\n2) Метрология\n3) Процессы формообразования и инструменты" + f"\n\n" + checkweek() + f"\nРасписание на Четвер:\n1) Иностранный язык\n2) МДК.04.01\n3) Физическая культура"
            if date.today().weekday() == 3:
                return checkweek() + f"\nРасписание на Четвер:\n1) Иностранный язык\n2) МДК.04.01\n3) Физическая культура" + f"\n\n" + checkweek() + f"\nРасписание на Пятницу:\n1) Русский язык и культура речи\n2) Электротехника и электроника\n3) Информатика"
            if date.today().weekday() == 4:
                return checkweek() + f"\nРасписание на Пятницу:\n1) Русский язык и культура речи\n2) Электротехника и электроника\n3) Информатика" + f"\n\n" + checkweek() + f"\nРасписание на Субботу:\n2) Техническая механика\n3) Инженерная графика\n4) Инженерная графика(над) или Процессы формообразования и инструменты(под)"
            if date.today().weekday() == 5:
                return weekday() + f"\nРасписание на Субботу:\n2) Техническая механика\n3) Инженерная графика\n4) Инженерная графика(над) или Процессы формообразования и инструменты(под)" + f"\n\n" + checkweek() + f"\nРасписание на Понедельник:\n1) Русский язык и культура речи(над) или МДК.04.01(под)\n2) Метрология\n3) Процессы формообразования и инструменты"
            if date.today().weekday() == 6:
                return checkweek() + f"\nРасписание на Понедельник:\n1) Русский язык и культура речи(над) или МДК.04.01(под)\n2) Метрология\n3) Процессы формообразования и инструменты"
            return

        # Команды
        elif message.upper() == self._COMMANDS[2]:
            return f"Весь список команд:\n1) Привет - приветствие с ботом.\n2) Расписание - показывает расписание на сегодня и на следующий день.\n3) Список - показывает всех студентов группы 18-4ТМ.\n4) Препод - показывает всех преподователей группы 18-4ТМ.\n5)Дз - посмотреть/добавить домашнее задание на завтра.\n6)Замены - посмотреть/добавить замены на завтра.\n7) Пока - прощание с ботом."

        # Помощь
        elif message.upper() == self._COMMANDS[3]:
            return f"Весь список команд:\n1) Привет - приветствие с ботом.\n2) Расписание - показывает расписание на сегодня и на следующий день.\n3) Список - показывает всех студентов группы 18-4ТМ.\n4) Препод - показывает всех преподователей группы 18-4ТМ.\n5)Дз - посмотреть/добавить домашнее задание на завтра.\n6)Замены - посмотреть/добавить замены на завтра.\n7) Пока - прощание с ботом."

        # Пока
        elif message.upper() == self._COMMANDS[4]:
            return f"Пока, {self._USERNAME}!"

        # аниме
        if message.upper().find(self._COMMANDS[5], 0) != -1:
            arg = message.upper().replace(self._COMMANDS[5] + " ", "")
            if (arg != "" and arg != "аниме"):
                return animelist(arg.lower().replace(',', '\n'))

        # список
        if message.upper() == self._COMMANDS[6]:
            return f"Список группы 18-4ТМ:\n1) Анишкевич Каролина Денисовна.\n2) Артамонов Николай Алексеевич.\n3) Битюков Кирилл Владимирович.\n4) Большаков Никита Сергеевич.\n5) Вдовин Никита Сергеевич.\n6) Горкина Валерия Алексеевна.\n7) Гущин Иван Владимирович.\n8) Демидов Михаил Дмитриевич.\n9) Зотимов Александр Юрьевич.\n10) Катков Николай Сергеевич.\n11) Коковихин Владимир Эдуардович.\n12) Коткова Екатерина Владимировна.\n13) Купцов Андрей Николаевич.\n14) Марков Максим Андреевич.\n15) ?\n16) Ногтев Кирилл Алексеевич.\n17) Пойманов Кирилл Вячеславович.\n18) Сидлярович Денис Андреевич.\n19) Синицын Павел Игоревич.\n20) Скирдонов Павел Владимирович.\n21) Судакова Евгения Александровна.\n22) Тимина Екатерина Александровна.\n23) Филоненко Ксения Николаевна.\n24) Шабаев Игорь Владимирович."

        # препод
        if message.upper() == self._COMMANDS[7]:
            return f"Список преподователей группы 18-4ТМ:\n1) Электротехника и электроника - Смирнова Ольга Георгиевна.\n2) Метрология - Заливчей Светлана Александровна.\n3) Процессы формообразования и инструменты - Заливчей Светлана Александровна.\n4) Бережливое производство - Скакодуб Алла Валентиновна.\n5) Информатика - Сидорова Оксана Юрьевна.\n6) Техническая механика - Леонова Елена Евгеньевна.\n7) Русский язык и культура речи - Куранова Юлия Васильевна.\n8) МДК.04.01 - Кошкина Светлана Александровна.\n9) Английский язык(1 группа) - Орлова Надия Хайдеровна.\n10) Английский язык(2 группа) - Пашанина Е.С.\n11) Физическая культура - Михайлов Владимир Юрьевич.\n12) Инженерная графика(1 группа) - Вилкова Светлана Викторовна.\n13) Инженерная графика(2 группа) - Горячева Александра Павловна."

        # acleardz
        if message.upper() == self._COMMANDS[8]:
            clearjsondz()
            return f"Списки с дз был очищен!"

        # aclearchange
        if message.upper() == self._COMMANDS[9]:
            clearjsonchange()
            return f"Спиcок с заменами был очищен!"

        # ДЗ
        if message.upper().find(self._COMMANDS[10], 0) != -1:
            arg = message.upper().replace(self._COMMANDS[10] + " ", "")
            uname = self._USERNAME
            if (arg != "" and arg != "ДЗ"):
                writedz(dzinfo=arg.lower().replace(',', ' '))
                if readdz() == "":
                    return f"На завтра нет дз"
                return f"ДЗ на завтра:\n" + readdz() + f"\nДобавил: " + uname
            elif (arg == "ДЗ" or arg == ""):
                if readdz() == "":
                    return f"На завтра нет дз"
                return f"ДЗ на завтра:\n" + readdz() + f"\nДобавил: " + uname
            else:
                return f"На завтра нет дз"

        # Замены
        if message.upper().find(self._COMMANDS[11], 0) != -1:
            arg = message.upper().replace(self._COMMANDS[11] + " ", "")
            uname = self._USERNAME
            if (arg != "" and arg != "ЗАМЕНЫ"):
                writechange(changeinfo=arg.lower().replace(',', ' '))
                if readchange() == "":
                    return f"На завтра нет замен"
                return f"Замены на завтра:\n" + readchange() + f"\nДобавил: " + uname
            elif (arg == "ЗАМЕНЫ" or arg == ""):
                if readchange() == "":
                    return f"На завтра нет замен"
                return f"Замены на завтра:\n" + readchange() + f"\nДобавил: " + uname
            else:
                return f"На завтра нет замен"

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
    
