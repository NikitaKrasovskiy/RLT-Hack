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


# Процесс размещения лота
def order_process(step):
    match step:
        case 0:
            send_request_message(id, 'Введите стоимость лота',
                                 keyboard_config.back_to_the_customer_interface())
            step += 1
        case 1:
            send_request_message(id, 'Введите дату окончания тендера в формате ДД.ММ.ГГГГ',
                                 keyboard_config.back_to_the_customer_interface())
            step += 1
        case 2:
            send_request_message(id, 'Ваш лот сформирован!',
                                 keyboard_config.back_to_the_customer_interface())
            step = 0
    return step


def body_request_message(person_id, some_message, keyboard_obj, keyboard_after, condition, user_obj):
    user_obj.change_condition(condition)
    keyboard_obj = keyboard_after
    send_request_message(person_id, some_message, keyboard_obj)
    return keyboard_obj, user_obj


# def import_data_to_db - метод для отправки данных о лоте в БД. Нужно проверять, что этого лота в базе данных нет!


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

            # Возврат в начальное меню
            elif message == 'вернуться в начало':
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard, keyboard_config.init_keyboard(), 'no_condition', user)
                print("Back to the start menu")

# ---------------------------------------------------------------------------------------
#   Обработка работы с пользователем в роли заказчика
# ---------------------------------------------------------------------------------------

            # Выбор роли заказчика
            elif (user.get_condition() == 'no_condition') & (message == 'я - заказчик'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard, keyboard_config.customer_keyboard(), 'customer', user)
                print("Input into customer")

            # Возврат в меню заказчика после/во время размещения лота
            elif (user.get_condition() in ['customer', 'ordered']) & (message == '1. вернуться в меню заказчика'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию', keyboard,
                                                      keyboard_config.customer_keyboard(), 'customer', user)

            # Выбор создания процедуры тендерных торгов в роли заказчика
            elif (user.get_condition() == 'customer') & (message == '3. создание процедуры'):
                keyboard, user = body_request_message(id, 'Введите наименование лота',
                                                      keyboard, keyboard_config.back_to_the_customer_interface(),
                                                      'ordered', user)
                order_data.append(str(id))
                print("Input into customer")

            #  Чтение данных для занесения в БД данных о лоте
            elif user.get_condition() == 'ordered':
                count = order_process(count)
                order_data.append(message)
                if count == 0:
                    for i in order_data:
                        print(i)
                    send_request_message(id, '\n'.join(order_data[1:]), keyboard_config.back_to_the_customer_interface())
                    order_data.clear()
                    keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию', keyboard,
                                                          keyboard_config.back_to_the_customer_interface(), 'customer',
                                                          user)
                print("Read data for order")

# ---------------------------------------------------------------------------------------
#   Обработка работы с пользователем в роли поставщика
# ---------------------------------------------------------------------------------------

            # Выбор роли поставщика
            elif (user.get_condition() == 'no_condition') & (message == 'я - поставщик'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard, keyboard_config.provider_keyboard(), 'provider', user)
                print("Input into provider")

            # Поиск торгов, выборка из 5-ти подходящих
            elif (user.get_condition() == 'provider') & (message == '3. поиск торгов'):
                keyboard, user = body_request_message(id, 'Перечень торгов',
                                                      keyboard, keyboard_config.back_to_the_provider_interface(), 'founder', user)
                # Нужем метод, который возвращает строки из БД
                # Из него берем первые 0-5 строк, через for отправляем сообщения
                print("Input into find tender")

            elif (user.get_condition() == 'founder') & (message == 'следующие'):
                keyboard, user = body_request_message(id, 'Перечень торгов',
                                                      keyboard, keyboard_config.back_to_the_provider_interface(),
                                                      'founder', user)
                print("Input into trade list")

            else:
                send_request_message(id, 'Не могу разобрать вашу команду. Пожалуйста, повторите запрос', keyboard)
                print('Wrong request')
            id = event.user_id

        if user.get_condition() != 'ordered':
            order_data.clear()
            count = 0
