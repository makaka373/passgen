import telebot
from itertools import product

BOT_TOKEN = "7378680396:AAHANuj2UlFX84pFJo7iplykjPbrx6fK6D0"
bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

def generate_password_list(keywords):
    """Генерация списка паролей на основе всех возможных комбинаций ключевых слов."""
    passwords = []
    for n in range(1, 4):  # Задаём количество слов в пароле (например, от 1 до 3)
        for combination in product(keywords, repeat=n):
            password = ''.join(combination)
            passwords.append(password)
    return passwords

@bot.message_handler(commands=["start"])
def start(message):
    """Начало работы с ботом."""
    bot.send_message(message.chat.id, "Привет! Введите 5 ключевых слов через пробел для генерации паролей.")

@bot.message_handler(func=lambda message: True)
def get_keywords(message):
    """Обработка ввода ключевых слов."""
    keywords = message.text.split()

    # Проверка количества ключевых слов.
    if len(keywords) != 5:
        bot.send_message(message.chat.id, "Введите ровно 5 ключевых слов через пробел.")
        return

    # Генерация паролей.
    passwords = generate_password_list(keywords)

    if passwords:
        bot.send_message(message.chat.id, f"Сгенерировано {len(passwords)} паролей. Вот примеры:")
        bot.send_message(message.chat.id, "\n".join(passwords[:10]))  # Показываем только первые 10 паролей.

        # Сохранение паролей в файл.
        with open("password_list.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(passwords))
        with open("password_list.txt", "rb") as file:
            bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, "Не удалось сгенерировать пароли.")

bot.polling()

