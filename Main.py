import random
import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from commander.commander import Commander
from vk_bot import VkBot
import datetime
import change_site
from threading import Timer
import os

def start():
    try:
        x = datetime.datetime.today()
        y = x.replace(day=x.day, hour=15, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        delta_t = y - x

        secs = delta_t.total_seconds()

        def write_msg(user_id, message):
            vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

        token = os.environ['VK_TOKEN']
        vk = vk_api.VkApi(token=token)
        longpoll = VkLongPoll(vk)
        commander = Commander()
        api = vk.get_api()
        print("Бот запущен")

        def send_message():
            i = 0
            while i < 4:
                users = [186003041, 288925718, 525452357, 187419279]
                change = "Замены на завтра: \n" + change_site.start()
                api.messages.send(user_id=users[i], message=change, random_id=get_random_id())
                print("Сообщение отправлено пользователю: " + str(users[i]))
                i = i + 1

        t = Timer(secs, send_message)
        t.start()

        for event in longpoll.listen():
            if event.attachments.items():
                continue
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    print(f'Новое сообщение от: {event.user_id}', end='')
                    bot = VkBot(event.user_id)
                    if event.text[0] == "":
                        write_msg(event.user_id, commander.do(event.text[1::]))
                    else:
                        write_msg(event.user_id, bot.new_message(event.text))
                    print('Текст: ', event.text)
                    print("-------------------")
    except:
        print("Перезапуск")
        start()

start()
