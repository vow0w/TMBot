import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from commander.commander import Commander
from vk_bot import VkBot
import os
import datetime
import time

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

token = os.environ['VK_TOKEN']
vk = vk_api.VkApi(token=token)
api = vk.get_api()
longpoll = VkLongPoll(vk)
commander = Commander()
print("Бот запущен")

#Рассылка
while True:
    if datetime.datetime.today().strftime('%H:%M') == "16:06":
        i = 0
        while i < 4:
            users = [186003041, 288925718, 525452357, 187419279]
            change = "Замены на завтра: \n" + change_site.start()
            api.messages.send(user_id=users[i], message=change, random_id=get_random_id())
            i = i + 1
    time.sleep(55)

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
