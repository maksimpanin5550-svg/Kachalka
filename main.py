import os
import telebot
from telebot import types
from dotenv import load_dotenv
import user_strength
import training_program

load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")

bot = telebot.TeleBot(TG_TOKEN)

last_messages = {}

def delete_old_message(chat_id):
    if chat_id in last_messages:
        try:
            bot.delete_message(chat_id, last_messages[chat_id])
        except:
            pass

@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'Назад')
def main(message):
    chat_id = message.chat.id
    bot.clear_step_handler_by_chat_id(chat_id)
    delete_old_message(chat_id)
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Мои Силовые'))
    markup.add(types.KeyboardButton('Моя Программа Тренировки'))

    sent_msg = bot.send_message(chat_id, 'Вы в Главном меню', reply_markup=markup)
    last_messages[chat_id] = sent_msg.message_id
    bot.register_next_step_handler(sent_msg, handle_main_commands)

def handle_main_commands(message):
    if message.text == 'Мои Силовые':
        user_strength.start_strength_input(bot, message, main)
    elif message.text == 'Моя Программа Тренировки':
        training_program.start_training_program(bot, message, main)
    else:
        main(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
