import telebot
from telebot import types

TOKEN = '6743059411:AAHxUZIxvit0joN32BuRQ8fMO7peXl6hA1E'
bot = telebot.TeleBot(TOKEN)

menu = {
    "завтрак": {
        "тост-авокадо": 120.99,
        "блины": 90.99,
        "омлет": 110.50,
        "гранола": 95.00,
        "фреш": 80.00,
        "кофе": 70.00,
        "чай": 50.00
    },
    "обед": {
        "бургер": 140.99,
        "салат": 100.50,
        "бутерброд": 80.99,
        "паста": 150.00,
        "рыба с картофелем": 170.00,
        "лимонад": 60.00,
        "сок": 65.00
    },
    "ужин": {
        "стейк": 240.99,
        "лапша": 180.50,
        "морепродукты": 220.99,
        "пицца": 200.00,
        "жаркое": 190.00,
        "вино": 120.00,
        "пиво": 80.00
    }
}

special_offer = {
    "завтрак": "К омлету мы предлагаем бесплатный кофе или чай!",
    "обед": "При заказе бургера - салат в подарок!",
    "ужин": "Ужин в компании - скидка 15% на второе блюдо!"
}

orders = {}


@bot.message_handler(commands=['start'])
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    brunch_button = types.KeyboardButton('Завтрак')
    lunch_button = types.KeyboardButton('Обед')
    dinner_button = types.KeyboardButton('Ужин')
    markup.add(brunch_button, lunch_button, dinner_button)
    bot.send_message(message.chat.id, "Добро пожаловать в наш ресторан! Пожалуйста, выберите вариант меню:",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if message.text.lower() in menu.keys():
        markup = types.InlineKeyboardMarkup()
        for item in menu[message.text.lower()]:
            button_text = f'{item} - ₽{menu[message.text.lower()][item]}'
            button = types.InlineKeyboardButton(text=button_text, callback_data=f'{message.text.lower()}_{item}')
            markup.add(button)
        bot.send_message(chat_id, f"{message.text.title()} меню:\n{special_offer.get(message.text.lower(), '')}",
                         reply_markup=markup)
    elif message.text.lower() == "нет" and chat_id in orders:
        total_price = sum(price * quantity for item, (price, quantity) in orders[chat_id].items())
        bot.send_message(chat_id, f"Сумма вашего заказа: ₽{total_price}. Спасибо за заказ!")
        del orders[chat_id]
        send_menu(message)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите подходящий вариант меню.")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    order_type, item = call.data.split('_')
    if chat_id not in orders:
        orders[chat_id] = {}
    if item in orders[chat_id]:
        orders[chat_id][item] = (menu[order_type][item], orders[chat_id][item][1] + 1)
    else:
        orders[chat_id][item] = (menu[order_type][item], 1)
    bot.send_message(chat_id, f"{item} добавлено в заказ! Что-то ещё? Если всё, напишите 'Нет'")


bot.polling()
