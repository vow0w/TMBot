import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from commander.commander import Commander
from vk_bot import VkBot

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

# API-ключ созданный ранее
token = "KEY_TOKEN"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

commander = Commander()
print("Бот запущен")
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
