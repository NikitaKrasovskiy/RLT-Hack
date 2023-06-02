import vk_api
import keyboard_config
from vk_api.longpoll import VkLongPoll, VkEventType
from __class_user__ import User


# BASIC METHODS

# Стартовое меню
def start_dialog(person_id, this_keyboard):
    person_name = session_api.users.get(user_ids=person_id, fields="first_name")
    vk_session.method("messages.send", {"user_id": person_id,
                                        "message": f"Приветствую Вас, {person_name[0]['first_name']}. Выберите интересующую Вас категорию",
                                        "random_id": 0,
                                        "keyboard": this_keyboard.get_keyboard()})


# Отправка обратного сообщения
def send_request_message(person_id, some_message, this_keyboard):
    vk_session.method("messages.send", {"user_id": person_id,
                                        "message": some_message,
                                        "random_id": 0,
                                        "keyboard": this_keyboard.get_keyboard()})


def body_request_message(person_id, some_message, keyboard_obj, keyboard_after, condition, user_obj):
    user_obj.change_condition(condition)
    keyboard_obj = keyboard_after
    send_request_message(person_id, some_message, keyboard_obj)
    return keyboard_obj, user_obj


vk_session = vk_api.VkApi(
    token='vk1.a.iDBLREQXWppl5hXXPCZTLiZ-evyY9F_e6hFe5A3EWlLojk30'
          'nugZSmJEqYhXJesa-zN_yt3p8ctK1JshWSn4_4Y6W26a7D5XZMG1JQQ'
          'OlPVRlZdzI-A6x_62I1zhF2G5oUrU7NF4Mj3Kph8faqZfaqPqVA2s9n'
          'MHR8TKSoRRX3d5FaAjNI7jnG4gDViuxA6nfOX_wmxIEzJOcZFCj3-UIA')
session_api = vk_session.get_api()

longpool = VkLongPoll(vk_session)
keyboard = keyboard_config.init_keyboard()
user = User()
count = 0
order_data = []

for event in longpool.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            message = event.text.lower()
            id = event.user_id

            # Первый этап в чат боте
            if (user.get_condition() == 'no_condition') & (message == 'начать'):
                start_dialog(id, keyboard)
                print("start dialog with person")

            # Выбор роли заказчика
            elif (user.get_condition() == 'no_condition') & (message == 'я - заказчик'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard, keyboard_config.customer_keyboard(), 'customer', user)
                print("Input into customer")

            # Выбор роли поставщика
            elif (user.get_condition() == 'no_condition') & (message == 'я - поставщик'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard, keyboard_config.provider_keyboard(), 'provider', user)
                print("Input into provider")

            # Возврат в начальное меню
            elif message == 'вернуться в начало':
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard, keyboard_config.init_keyboard(), 'no_condition', user)
                print("Back to the start menu")

            # Выбор создания процедуры тендерных торгов в роли заказчика
            elif (user.get_condition() == 'customer') & (message == '3. создание процедуры'):
                keyboard, user = body_request_message(id, 'Введите наименование лота',
                                                      keyboard, keyboard_config.back_to_the_customer_interface(),
                                                      'ordered', user)
                order_data.append(id)

            elif (user.get_condition() in ['customer', 'ordered']) & (message == '1. вернуться в меню заказчика'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию', keyboard,
                                                      keyboard_config.customer_keyboard(), 'customer', user)
                order_data.clear()
                count = 0

            #  Чтение данных для занесения в БД данных о лоте
            elif user.get_condition() == 'ordered':
                match count:
                    case 0:
                        send_request_message(id, 'Введите стоимость лота',
                                             keyboard_config.back_to_the_customer_interface())
                        count += 1
                    case 1:
                        send_request_message(id, 'Введите дату окончания тендера в формате ДД.ММ.ГГГГ',
                                             keyboard_config.back_to_the_customer_interface())
                        count += 1
                    case 2:
                        send_request_message(id, 'Ваш лот сформирован!',
                                             keyboard_config.back_to_the_customer_interface())
                        count = 0
                order_data.append(message)
                if count == 0:
                    for i in order_data:
                        print(i)
                    order_data.clear()
                    keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию', keyboard,
                                                          keyboard_config.back_to_the_customer_interface(), 'customer',
                                                          user)


            else:
                send_request_message(id, 'Не могу разобрать вашу команду. Пожалуйста, повторите запрос', keyboard)
                print('Wrong request')
