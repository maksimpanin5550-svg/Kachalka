from telebot import types

user_training_data = {}

def start_training_program(bot, message, main_menu_callback):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Создать новую программу', 'Просмотреть программу', 'Редактировать упражнение', 'Назад')
    msg = bot.send_message(chat_id, 'Программа тренировок\nИспользуйте меню для управления планом.', reply_markup=markup)
    bot.register_next_step_handler(msg, lambda m: handle_training_command(bot, m, main_menu_callback))

def handle_training_command(bot, message, main_menu_callback):
    if message.text == 'Создать новую программу':
        start_new_training(bot, message, main_menu_callback)
    elif message.text == 'Просмотреть программу':
        view_training_program(bot, message, main_menu_callback)
    elif message.text == 'Редактировать упражнение':
        bot.send_message(message.chat.id, "Редактирование в разработке.")
        start_training_program(bot, message, main_menu_callback)
    elif message.text == 'Назад':
        main_menu_callback(message)
    else:
        start_training_program(bot, message, main_menu_callback)

def start_new_training(bot, message, main_menu_callback):
    chat_id = message.chat.id
    user_training_data[chat_id] = {'program_name': '', 'exercises': [], 'current_exercise': None, 'step': 0}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Отмена')
    msg = bot.send_message(chat_id, 'Введите название программы:', reply_markup=markup)
    bot.register_next_step_handler(msg, lambda m: process_training_input(bot, m, main_menu_callback))

def process_training_input(bot, message, main_menu_callback):
    chat_id = message.chat.id
    text = message.text
    if text == 'Отмена':
        start_training_program(bot, message, main_menu_callback)
        return
    data = user_training_data.get(chat_id)
    if not data:
        start_training_program(bot, message, main_menu_callback)
        return

    if data['step'] == 0:
        data['program_name'] = text
        data['step'] = 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Пропустить', 'Отмена')
        msg = bot.send_message(chat_id, f'Программа: {text}\nВведите название упражнения:', reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: process_training_input(bot, m, main_menu_callback))
    elif data['step'] == 1:
        if text == 'Пропустить':
            show_program_menu(bot, message, main_menu_callback)
            return
        data['current_exercise'] = {'name': text, 'sets': ''}
        data['step'] = 2
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Пропустить', 'Отмена')
        msg = bot.send_message(chat_id, f'Упражнение: {text}\nВведите подходы (например, 4x10):', reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: process_training_input(bot, m, main_menu_callback))
    elif data['step'] == 2:
        data['current_exercise']['sets'] = 'не указано' if text == 'Пропустить' else text
        data['exercises'].append(data['current_exercise'])
        data['step'] = 3
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Добавить еще упражнение', 'Завершить')
        msg = bot.send_message(chat_id, f'Добавлено. Всего: {len(data["exercises"])}', reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: process_training_input(bot, m, main_menu_callback))
    elif data['step'] == 3:
        if text == 'Добавить еще упражнение':
            data['step'] = 1
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Пропустить', 'Отмена')
            msg = bot.send_message(chat_id, 'Введите название упражнения:', reply_markup=markup)
            bot.register_next_step_handler(msg, lambda m: process_training_input(bot, m, main_menu_callback))
        else:
            show_program_menu(bot, message, main_menu_callback)

def show_program_menu(bot, message, main_menu_callback):
    chat_id = message.chat.id
    data = user_training_data.get(chat_id, {})
    text = f"Программа: {data.get('program_name')}\n\n"
    for i, ex in enumerate(data.get('exercises', []), 1):
        text += f"{i}. {ex['name']} — {ex['sets']}\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Добавить упражнение', 'Удалить программу', 'Назад')
    msg = bot.send_message(chat_id, text if data.get('exercises') else "Пусто", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda m: process_program_menu_command(bot, m, main_menu_callback))

def process_program_menu_command(bot, message, main_menu_callback):
    if message.text == 'Добавить упражнение':
        user_training_data[message.chat.id]['step'] = 1
        msg = bot.send_message(message.chat.id, 'Название упражнения:', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена'))
        bot.register_next_step_handler(msg, lambda m: process_training_input(bot, m, main_menu_callback))
    elif message.text == 'Удалить программу':
        user_training_data.pop(message.chat.id, None)
        bot.send_message(message.chat.id, 'Удалено.')
        start_training_program(bot, message, main_menu_callback)
    else:
        start_training_program(bot, message, main_menu_callback)

def view_training_program(bot, message, main_menu_callback):
    if message.chat.id not in user_training_data:
        bot.send_message(message.chat.id, "Нет программ.")
        start_training_program(bot, message, main_menu_callback)
    else:
        show_program_menu(bot, message, main_menu_callback)