import vk_api
import keyboard_config
from vk_api.longpoll import VkLongPoll, VkEventType
from __class_user__ import User
from vk_api.keyboard import VkKeyboard

# BASIC METHODS


def start_dialog(person_id, this_keyboard):
    person_name = session_api.users.get(user_ids=person_id, fields="first_name")
    vk_session.method("messages.send", {"user_id": person_id,
                                        "message": f"Приветствую Вас, {person_name[0]['first_name']}. Выберите интересующую Вас категорию",
                                        "random_id": 0,
                                        "keyboard": this_keyboard.get_keyboard()})


def send_request_message(person_id, some_message, this_keyboard):
    vk_session.method("messages.send", {"user_id": person_id,
                                        "message": some_message,
                                        "random_id": 0,
                                        "keyboard": this_keyboard.get_keyboard()})


def change_user_scenario(scenario):
    person = User()
    person.change_condition(scenario)
    return person


vk_session = vk_api.VkApi(

    token='vk1.a.iDBLREQXWppl5hXXPCZTLiZ-evyY9F_e6hFe5A3EWlLojk30'
          'nugZSmJEqYhXJesa-zN_yt3p8ctK1JshWSn4_4Y6W26a7D5XZMG1JQQ'
          'OlPVRlZdzI-A6x_62I1zhF2G5oUrU7NF4Mj3Kph8faqZfaqPqVA2s9n'
          'MHR8TKSoRRX3d5FaAjNI7jnG4gDViuxA6nfOX_wmxIEzJOcZFCj3-UIA')

session_api = vk_session.get_api()

longpool = VkLongPoll(vk_session)

keyboard = keyboard_config.init_keyboard()

user = User()

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.text.lower()
            id = event.user_id
            if (user.get_condition() == 'None') & (message == 'начать'):
                start_dialog(id, keyboard)
                print("start dialog with person")
            elif (user.get_condition() == 'None') & (message == 'я - заказчик'):
                user = change_user_scenario('customer')
                keyboard = keyboard_config.customer_keyboard()
                send_request_message(id, 'Выберите интересующую Вас категорию', keyboard)
            elif (user.get_condition() == 'None') & (message == 'я - поставщик'):
                user = change_user_scenario('provider')
                keyboard = keyboard_config.provider_keyboard()
                send_request_message(id, 'Выберите интересующую Вас категорию', keyboard)
            # elif message == 'я - новичок'
            #     new_scenario(id)
            elif message == '5. Вернуться в начало':
                user = change_user_scenario('None')
                keyboard = keyboard_config.init_keyboard()
                send_request_message(id, 'Выберите интересующую Вас категорию', keyboard)
            else:
                send_request_message(id, 'Не могу разобрать вашу команду. Пожалуйста, повторите запрос', keyboard)
                print('Wrong request')


