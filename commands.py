import requests
import bs4
from secondNameParse import findFullName

commandsList = ["привет", "препод", "расписание"]


class Bot:
    def __init__(self, user_id):
        print("\nСоздан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = commandsList

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")
        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        name = user_name.split()[0]
        return name

    def new_message(self, message):
        # command: Привет
        if message.lower() == self._COMMANDS[0]:
            return f"Здравствуй, {self._USERNAME}!"
        # command: Препод
        elif message.split()[0].lower() == self._COMMANDS[1]:
            try:
                secondName = message.split()[1]
            except IndexError:
                secondName = ""

            if secondName != "":
                return f"Найден преподователь:\n{findFullName(secondName)}"
            else:
                return "Вы не ввели фамилию преподователя!"
        # command: Расписание
        elif message.lower() == self._COMMANDS[2]:
            pass

        else:
            return f"Команда не найдена: {message.lower()}"

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
