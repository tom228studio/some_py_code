import json
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import main_token

vk_session = vk_api.VkApi(token=main_token)
longpoll = VkLongPoll(vk_session)


class User:

    def __init__(self, idppl, mode, cash):
        self.id = idppl
        self.mode = mode
        self.cash = cash


def get_keyboard(buts):
    nb = []
    color = ''
    for i in range(len(buts)):
        nb.append([])
        for k in range(len(buts[i])):
            nb[i].append(None)
    for i in range(len(buts)):
        for k in range(len(buts[i])):
            text = buts[i][k][0]
            color = {'зелёный': 'positive', 'красный': 'negative', 'синий': 'primary'}[buts[i][k][1]]
            nb[i][k] = {"action": {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"},
                        "color": f"{color}"}
    first_keyboard = {'one_time': False, 'buttons': nb}
    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
    first_keyboard = str(first_keyboard.decode('utf-8'))
    return first_keyboard


after_key = get_keyboard([
    [('начать', 'зелёный')]
])

start_key = get_keyboard([
    [('кнопка 1', 'зелёный'), ('кнопка 2', 'зелёный'), ('кнопка 3', 'зелёный')]
])


def sender(id, text, key):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0, 'keyboard': key})


users = []

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.from_chat:

                idppl = event.user_id
                id = event.chat_id
                msg = event.text.lower()

                if msg == 'начать квест бам':
                    sender(id, '1', after_key)
                    time.sleep(60)
                    sender(id, '2', after_key)
                    time.sleep(60)
                    sender(id, '3', after_key)

                if msg == 'привет':
                    sender(id, 'Привет хохол', after_key)

                if msg == 'начать':
                    flag1 = 0
                    for user in users:
                        if user.id == idppl:
                            sender(id, 'Выбирите действие', start_key)
                            user.mode = 'start'
                            flag1 = 1
                    if flag1 == 0:
                        users.append(User(idppl, 'start', 0))
                        sender(id, 'Выбирите действие', start_key)

                for user in users:
                    if user.id == idppl:

                        if user.mode == 'start':
                            if msg == f'кнопка 1':
                                sender(id, f'Ваш баланс: {user.cash}', start_key)
                            if msg == 'кнопка 2':
                                sender(id, f'Ваш баланс: {user.cash}', start_key)

                        if user.mode == 'game':
                            sender(id, f'Ваш баланс: {user.cash}', start_key)
