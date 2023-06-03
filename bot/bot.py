import vk_api
import keyboard_config
import phrase_list
from vk_api.longpoll import VkLongPoll, VkEventType
from __class_user__ import User
from database.main import Order, OKVED
import psycopg2
import json


# BASIC METHODS

# Стартовое меню
def start_dialog(person_id, this_keyboard):
    person_name = session_api.users.get(user_ids=person_id, fields="first_name")
    vk_session.method("messages.send", {"user_id": person_id,
                                        "message": f"Приветствую Вас, {person_name[0]['first_name']}. Выберите "
                                                   f"интересующую Вас категорию",
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
    # match step:
    if step == 0:
        send_request_message(id, 'Введите стоимость лота',
                             keyboard_config.back_to_the_customer_interface())
        step += 1
    elif step == 1:
        send_request_message(id, 'Введите дату окончания тендера в формате ДД.ММ.ГГГГ',
                             keyboard_config.back_to_the_customer_interface())
        step += 1
    elif step == 2:
        send_request_message(id, 'Ваш лот сформирован!',
                             keyboard_config.back_to_the_customer_interface())
        step = 0
    return step


# Создание лота и занесение его в массив для дальнейшей отправки в БД
def create_order(step, data, vk_keyboard, msg):
    step = order_process(step)
    data.append(msg)
    if step == 0:
        for i in data:
            print(i)
        send_request_message(id, '\n'.join(data[1:]), vk_keyboard)
    return step, data


# Размещение запроса с выбором клавиатуры для пользователя и изменения сущности User
def body_request_message(person_id, some_message, keyboard_after, condition, user_obj):
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


            # Возврат в начальное меню
            elif message == 'вернуться в начало':
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard_config.init_keyboard(), 'no_condition', user)
                print("Back to the start menu")

            # Услуги РосЭлТорг
            elif message == 'услуги':
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас услугу, предоставляемую Росэлторг',
                                                      keyboard_config.service_keyboard(), 'serviced', user)
                print("Input into service menu")

            # ---------------------------------------------------------------------------------------
            #   Обработка работы с пользователем в роли заказчика
            # ---------------------------------------------------------------------------------------

            # Выбор роли заказчика
            elif (user.get_condition() == 'no_condition') & (message == 'я - заказчик'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard_config.customer_keyboard(), 'customer', user)
                print("Input into customer")

            # Возврат в меню заказчика после/во время размещения лота
            elif (user.get_condition() in ['customer', 'ordered']) & (message == 'вернуться в меню заказчика'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard_config.customer_keyboard(), 'customer', user)

            # Выбор создания процедуры тендерных торгов в роли заказчика
            elif (user.get_condition() == 'customer') & (message == 'создание процедуры'):
                keyboard, user = body_request_message(id, 'Введите наименование лота',
                                                      keyboard_config.back_to_the_customer_interface(),
                                                      'ordered', user)
                order_data.append(str(id))
                print("Input into customer")

            # Чтение данных для занесения в БД данных о лоте
            elif user.get_condition() == 'ordered':
                count, order_data = create_order(count, order_data, keyboard_config.back_to_the_customer_interface(),
                                                 message)
                if count == 0:
                    order = Order(order_data[1], order_data[2], order_data[3], order_data[0])
                    order.test_fun(order_data)
                    test = order.select_orders_by_user_vk_id(int(order_data[0]))
                    print(test[1])
                    order_data.clear()
                    keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                          keyboard_config.back_to_the_customer_interface(), 'customer',
                                                          user)
                print("Read data for order")

            # ---------------------------------------------------------------------------------------
            #   Обработка работы с пользователем в роли поставщика
            # ---------------------------------------------------------------------------------------

            # Выбор роли поставщика
            elif (user.get_condition() == 'no_condition') & (message == 'я - поставщик'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard_config.provider_keyboard(), 'provider', user)
                print("Input into provider")

            # Поиск торгов, выборка из 5-ти подходящих
            elif (user.get_condition() == 'provider') & (message == 'поиск торгов'):
                keyboard, user = body_request_message(id, 'Перечень торгов',
                                                      keyboard_config.back_to_the_provider_interface(), 'founder', user)
                # Нужем метод, который возвращает строки из БД
                # TODO
                okved = OKVED()
                test = okved.get_by_okved_name("1")
                print(test  ыфтьс фылс фыгсфыгсмымсщмсофЫС73к730красовсицлисиии)
                # Из него берем первые 0-5 строк, через for отправляем сообщения
                print("Input into find tender")

            elif (user.get_condition() == 'founder') & (message == 'следующие'):
                keyboard, user = body_request_message(id, 'Перечень торгов',
                                                      keyboard_config.back_to_the_provider_interface(),
                                                      'founder', user)
                # Нужем метод, который возвращает строки из БД
                # Из него берем следующие 0-5 строк, через for отправляем сообщения
                # cout увеличиваем на 1
                print("Input into trade list")

            elif (user.get_condition() == 'founder') & (message == 'предыдущие'):
                keyboard, user = body_request_message(id, 'Перечень торгов',
                                                      keyboard_config.back_to_the_provider_interface(), 'founder', user)
                # Нужем метод, который возвращает строки из БД
                # Из него берем предыдущие 0-5 строк, через for отправляем сообщения
                # cout уменьшаем на 1 и проверяем, что count > 0
                print("Input into trade list")
            elif (user.get_condition() == 'founder') & (message == 'вернуться в меню поставщика'):
                keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                      keyboard_config.provider_keyboard(), 'provider', user)

            # ---------------------------------------------------------------------------------------
            #   Интерфейс нового пользователя
            # ---------------------------------------------------------------------------------------

            elif message == 'я - новичок':
                keyboard, user = body_request_message(id, phrase_list.newbie_start_phrase,
                                                      keyboard_config.newbie_keyboard(), 'newbie', user)
                print("Input into newbie root")

            elif (user.get_condition() == 'newbie') & (message == 'пройти курс'):
                keyboard, user = body_request_message(id, phrase_list.newbie_learn_curse,
                                                      keyboard_config.newbie_learning_courses(), 'newbie_learn', user)
                print("Input into newbie root")


            # ---------------------------------------------------------------------------------------
            #   Обработка работы с новым пользователем (в роли заказчика)
            # ---------------------------------------------------------------------------------------

            elif (user.get_condition() == 'newbie') & (message == 'я - заказчик'):
                keyboard, user = body_request_message(id, phrase_list.newbie_customer_phrase,
                                                      keyboard_config.customer_keyboard(), 'newbie', user)
                print("Input into newbie root/customer")

            elif (user.get_condition() == 'newbie') & (message == 'создание процедуры'):
                keyboard, user = body_request_message(id, 'Введите наименование лота',
                                                      keyboard_config.back_to_the_customer_interface(),
                                                      'newbie_ordered', user)
                order_data.append(str(id))
                print("Input into customer")

            elif (user.get_condition() == 'newbie') & (message == 'вернуться в меню заказчика'):
                keyboard, user = body_request_message(id, phrase_list.newbie_customer_phrase,
                                                      keyboard_config.customer_keyboard(), 'newbie', user)

            elif user.get_condition() == 'newbie_ordered':
                count, order_data = create_order(count, order_data, keyboard_config.back_to_the_customer_interface(),
                                                 message)
                if count == 0:
                    order_data.clear()
                    keyboard, user = body_request_message(id, 'Выберите интересующую Вас категорию',
                                                          keyboard_config.back_to_the_customer_interface(), 'newbie',
                                                          user)
                print("Read data for order")

            # ---------------------------------------------------------------------------------------
            #   Обработка работы с новым пользователем (в роли поставщика)
            # ---------------------------------------------------------------------------------------

            # Выбор роли поставщика (новичок)
            elif (user.get_condition() == 'newbie') & (message == 'я - поставщик'):
                keyboard, user = body_request_message(id, phrase_list.newbie_provider_phrase,
                                                      keyboard_config.provider_keyboard(), 'newbie', user)
                print("Input into customer(newbie)")

                # Поиск торгов, выборка из 5-ти подходящих
            elif (user.get_condition() == 'newbie') & (message == 'поиск торгов'):
                keyboard, user = body_request_message(id, 'Перечень торгов',
                                                      keyboard_config.back_to_the_provider_interface(),
                                                      'newbie_founder', user)
                # Нужем метод, который возвращает строки из БД
                # Из него берем первые 0-5 строк, через for отправляем сообщения
                print("Input into find tender")

            elif (user.get_condition() == 'newbie_provider') & (message == 'следующие'):
                keyboard, user = body_request_message(id, 'Перечень торгов',
                                                      keyboard_config.back_to_the_provider_interface(),
                                                      'newbie_founder', user)
                # Нужем метод, который возвращает строки из БД
                # Из него берем следующие 0-5 строк, через for отправляем сообщения
                # cout увеличиваем на 1
                print("Input into trade list")

            elif (user.get_condition() == 'newbie_provider') & (message == 'предыдущие'):
                keyboard, user = body_request_message(id, 'Перечень торгов',
                                                      keyboard_config.back_to_the_provider_interface(),
                                                      'newbie_founder', user)
                # Нужем метод, который возвращает строки из БД
                # Из него берем предыдущие 0-5 строк, через for отправляем сообщения
                # cout уменьшаем на 1 и проверяем, что count > 0
                print("Input into trade list")

            elif (user.get_condition() == 'newbie_founder') & (message == 'вернуться в меню поставщика'):
                keyboard, user = body_request_message(id, phrase_list.newbie_provider_phrase,
                                                      keyboard_config.provider_keyboard(), 'newbie', user)

            else:
                send_request_message(id, 'Не могу разобрать вашу команду. Пожалуйста, повторите запрос', keyboard)
                print('Wrong request')

        if user.get_condition() not in ['ordered', 'newbie_ordered']:
            order_data.clear()
            count = 0
