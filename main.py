from telebot import *
TOKEN="8774901021:AAGHY59GIjUjgoD1xiER_9PzJFjxeuL3eP0"
bot = telebot.TeleBot(TOKEN)

import logging
logging.basicConfig(level=logging.DEBUG)





# Вспомогательная функция для шифрования/дешифрования
def caesar_cipher(text, shift, mode='encrypt'):
    if mode == 'decrypt':
        shift = -shift
    
    result = ""
    for char in text:
        if char.isalpha():
            # Определяем границы алфавита (RU или EN)
            start_code = ord('а') if 'а' <= char.lower() <= 'я' else ord('a')
            alphabet_size = 32 if 'а' <= char.lower() <= 'я' else 26
            
            # Сохраняем регистр
            base = ord('А') if char.isupper() and alphabet_size == 32 else (ord('A') if char.isupper() else start_code)
            
            # Вычисляем новый символ
            shifted_char = chr((ord(char) - base + shift) % alphabet_size + base)
            result += shifted_char
        else:
            # Символы, не являющиеся буквами (пробелы, знаки), не меняем
            result += char
    return result

# Хранилище временных данных пользователя (не для продакшена, но для примера сойдет)
user_data = {}



@bot.message_handler(commands=["start"])
def hi(message):
    bot.send_message(message.chat.id, "Привет! Я - MLB, бoт по зашифрoвкe u рacшифрoвкe тeкстoвыx сoобщeний. \n"
    "Зашифровка сообщений выполняется с помощью команды /encryption \n"
    "Расшифровка сoобщений выполняется с помощью команды /transcript \n")
    
@bot.message_handler(commands=["encryption"])
def en(message):
    markup = types.                    ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Зашифровать 🔒")
    markup.add(item1)
    bot.send_message(message.chat.id, "Нажми на опцию ниже:",reply_markup=markup)
    
@bot.message_handler(commands=["transcript"])
def en(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item2 = types.KeyboardButton("Расшифровать 🔓")
    markup.add(item2)
    
    bot.send_message(message.chat.id, "Нажми на опцию ниже:", reply_markup=markup)
    


    




@bot.message_handler(func=lambda message: message.text in ["Зашифровать 🔒", "Расшифровать 🔓"])
def handle_mode(message):
    mode = 'encrypt' if "Зашифровать" in message.text else 'decrypt'
    user_data[message.chat.id] = {'mode': mode}
    
    msg = bot.send_message(message.chat.id, "Введите шаг шифра (целое число, например, 3):")
    bot.register_next_step_handler(msg, process_shift_step)

def process_shift_step(message):
    try:
        shift = int(message.text)
        user_data[message.chat.id]['shift'] = shift
        msg = bot.send_message(message.chat.id, "Теперь введите текст сообщения:")
        bot.register_next_step_handler(msg, process_cipher_step)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Ошибка! Нужно ввести целое число. Попробуйте еще раз:")
        bot.register_next_step_handler(msg, process_shift_step)

def process_cipher_step(message):
    data = user_data.get(message.chat.id)
    if not data:
        return send_welcome(message)
    
    text = message.text
    shift = data['shift']
    mode = data['mode']
    
    result = caesar_cipher(text, shift, mode)
    
    status = "Зашифрованный" if mode == 'encrypt' else "Расшифрованный"
    bot.send_message(message.chat.id, f"✅ **{status} текст:**\n\n`{result}`", parse_mode="Markdown")


   
   
@bot.message_handler(content_types=["text"])
def hi2(message):
    if message.text.lower()=='привет':
        bot.send_message(message.chat.id,"Привет дорогой пользователь!")

    
    
    
    ##########################
@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id,"Неопознанное сообщение.")
        
    
if __name__ == '__main__':
    print("Бот успешно запущен")
    bot.infinity_polling()
else:
    print('Ошибка запуска.')