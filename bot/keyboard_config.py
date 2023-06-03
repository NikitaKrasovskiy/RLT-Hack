from vk_api.keyboard import VkKeyboardButton, VkKeyboardColor, VkKeyboard


def init_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Я - заказчик', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Я - поставщик', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Я - новичок', VkKeyboardColor.PRIMARY)
    return keyboard


# Заказчик
def customer_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_openlink_button('1. Получить ЭЦП', 'https://www.roseltorg.ru/ecp')
    keyboard.add_line()
    keyboard.add_openlink_button('2. Регистрация в ЕИС', 'https://zakupki.gov.ru/epz/main/public/home.html')
    keyboard.add_line()
    keyboard.add_button('3. Создание процедуры')
    keyboard.add_line()
    keyboard.add_button('4. Мои заказы')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


# Поставщик
def provider_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_openlink_button('1. Получить ЭЦП', 'https://www.roseltorg.ru/ecp')
    keyboard.add_line()
    keyboard.add_openlink_button('2. Регистрация в ЕИС', 'https://zakupki.gov.ru/epz/main/public/home.html')
    keyboard.add_line()
    keyboard.add_button('3. Поиск торгов')
    keyboard.add_line()
    keyboard.add_button('4. Избранные торги')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


# Возврат в начальное меню
def back_to_the_start():
    keyboard = VkKeyboard()
    keyboard.add_openlink_button('Вернуться в начало')
    return keyboard


# Возврат в меню заказчика
def back_to_the_customer_interface():
    keyboard = VkKeyboard()
    keyboard.add_button('1. Вернуться в меню заказчика')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


# Возврат в меню поставщика
def back_to_the_provider_interface():
    keyboard = VkKeyboard()
    keyboard.add_button('1. Вернуться в меню поставщика')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


def trade_filter():
    pass