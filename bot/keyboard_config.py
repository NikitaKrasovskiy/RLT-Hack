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
    return keyboard


def trade_filter():
    pass

