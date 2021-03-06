from vk_api.longpoll import VkLongPoll, VkEventType
from config import token, idAdmin
import vk_api
from commands import Bot
from vk_api.utils import get_random_id
from secondNameParse import startSecondNameParse

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
api = vk.get_api()


def sendMessage(user_id, message):
    api.messages.send(user_id=user_id, message=message, random_id=get_random_id())


def start():
    print("Бот 18-4 ТМ включён")
    for event in longpoll.listen():
        if event.attachments.items():
            continue

        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                # admin listener
                if event.user_id == idAdmin:
                    # Command: update
                    if event.message == "!update":
                        startSecondNameParse()
                        continue
                    elif event.message == "!stop":
                        quit()

                # user listener
                print(f'Новое сообщение от: {event.user_id}', end='')
                bot = Bot(event.user_id)
                if event.text[0] != "":
                    sendMessage(event.user_id, bot.new_message(event.text))
                    print('Сообщение: ', event.text)
                    print("------------------------------")


if __name__ == "__main__":
    start()
