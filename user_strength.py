from telebot import types

user_data = {}

def get_back_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Сбросить рекорды'))
    markup.add(types.KeyboardButton('Назад'))
    return markup

def start_strength_input(bot, message, main_menu_callback):
    chat_id = message.chat.id
    if chat_id in user_data and 'deadlift' in user_data[chat_id]:
        data = user_data[chat_id]
        text = (f"Ваши показатели:\n\n"
                f"Жим Лёжа = {data.get('bench')} кг\n"
                f"Присед = {data.get('squat')} кг\n"
                f"Становая = {data.get('deadlift')} кг")
        msg = bot.send_message(chat_id, text, reply_markup=get_back_markup())
        bot.register_next_step_handler(msg, lambda m: handle_strength_menu(bot, m, main_menu_callback))
    else:
        sent_msg = bot.send_message(chat_id, "Введите вес для Жима Лёжа:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(sent_msg, lambda m: get_bench(bot, m, main_menu_callback))

def handle_strength_menu(bot, message, main_menu_callback):
    chat_id = message.chat.id
    if message.text == 'Назад':
        main_menu_callback(message)
    elif message.text == 'Сбросить рекорды':
        if chat_id in user_data:
            del user_data[chat_id]
        bot.send_message(chat_id, "Рекорды успешно сброшены.")
        start_strength_input(bot, message, main_menu_callback)
    else:
        start_strength_input(bot, message, main_menu_callback)

def get_bench(bot, message, main_menu_callback):
    user_data[message.chat.id] = {'bench': message.text}
    sent_msg = bot.send_message(message.chat.id, "Введите вес для Приседа:")
    bot.register_next_step_handler(sent_msg, lambda m: get_squat(bot, m, main_menu_callback))

def get_squat(bot, message, main_menu_callback):
    if message.chat.id not in user_data: user_data[message.chat.id] = {}
    user_data[message.chat.id]['squat'] = message.text
    sent_msg = bot.send_message(message.chat.id, "Введите вес для Становой:")
    bot.register_next_step_handler(sent_msg, lambda m: get_deadlift(bot, m, main_menu_callback))

def get_deadlift(bot, message, main_menu_callback):
    if message.chat.id not in user_data: user_data[message.chat.id] = {}
    user_data[message.chat.id]['deadlift'] = message.text
    msg = bot.send_message(message.chat.id, "Данные успешно сохранены!", reply_markup=get_back_markup())
    bot.register_next_step_handler(msg, lambda m: handle_strength_menu(bot, m, main_menu_callback))
