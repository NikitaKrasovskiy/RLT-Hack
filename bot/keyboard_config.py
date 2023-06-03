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
    keyboard.add_openlink_button('Получить ЭЦП', 'https://www.roseltorg.ru/ecp')
    keyboard.add_line()
    keyboard.add_openlink_button('Регистрация в ЕИС', 'https://zakupki.gov.ru/epz/main/public/home.html')
    keyboard.add_line()
    keyboard.add_button('Создание процедуры')
    keyboard.add_line()
    keyboard.add_button('Мои заказы')
    keyboard.add_line()
    keyboard.add_button('Услуги')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


# Поставщик
def provider_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_openlink_button('Получить ЭЦП', 'https://www.roseltorg.ru/ecp')
    keyboard.add_line()
    keyboard.add_openlink_button('Регистрация в ЕИС', 'https://zakupki.gov.ru/epz/main/public/home.html')
    keyboard.add_line()
    keyboard.add_button('Поиск торгов')
    keyboard.add_line()
    keyboard.add_button('Избранные торги')
    keyboard.add_line()
    keyboard.add_button('Услуги')
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
    keyboard.add_button('Вернуться в меню заказчика')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


# Возврат в меню поставщика
def back_to_the_provider_interface():
    keyboard = VkKeyboard()
    keyboard.add_button('Вернуться в меню поставщика')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


# Предложение услуг
def service_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_openlink_button('Электронные подписи', 'https://www.roseltorg.ru/ecp')
    keyboard.add_line()
    keyboard.add_openlink_button('Кредит на исполнение контракта', 'https://www.roseltorg.ru/credit-execution-contract')
    keyboard.add_openlink_button('Помощь в регистрации', 'https://www.roseltorg.ru/speed')
    keyboard.add_line()
    keyboard.add_openlink_button('Комплаенс проверка', 'https://www.roseltorg.ru/compliance')
    keyboard.add_openlink_button('Банковские гарантии', 'https://www.roseltorg.ru/bg')
    keyboard.add_line()
    keyboard.add_openlink_button('Сопровождение на торгах', 'https://www.roseltorg.ru/realty-support')
    keyboard.add_openlink_button('Экспертиза тендерной заявки', 'https://www.roseltorg.ru/bid')
    keyboard.add_line()
    keyboard.add_openlink_button('Обучающий центр', 'https://www.roseltorg.ru/education')
    keyboard.add_openlink_button('Специальные счета', 'https://www.roseltorg.ru/specschet')
    keyboard.add_line()
    keyboard.add_openlink_button('ЭДО \"Росинвойс\"', 'https://www.roseltorg.ru/edo')
    keyboard.add_openlink_button('Центр импортозамещения', 'https://www.roseltorg.ru/import')
    keyboard.add_line()
    keyboard.add_openlink_button('Сертификация продукции', 'https://www.roseltorg.ru/certification-center')
    keyboard.add_openlink_button('Страхование СМР', 'https://www.roseltorg.ru/insurance-fkr')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


# Клавиатура новичка, пробующего разные роли
def newbie_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Я - заказчик', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Я - поставщик', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Пройти курс', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_openlink_button('Чат для новичков', 'http://example.com/')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


# Обучающие курсы
def newbie_learning_courses():
    keyboard = VkKeyboard()
    keyboard.add_openlink_button('Обучающие курсы', 'https://www.roseltorg.ru/education')
    keyboard.add_line()
    keyboard.add_openlink_button('Вконтакте', 'http://example.com/')
    keyboard.add_line()
    keyboard.add_openlink_button('YouTube', 'http://example.com/')
    keyboard.add_line()
    keyboard.add_button('Вернуться в начало')
    return keyboard


def trade_filter():
    pass