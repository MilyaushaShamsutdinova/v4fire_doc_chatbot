import os
import telebot
from dotenv import load_dotenv
import re
from src.backend.pipeline import get_response
import time


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


def format_text(text):
    """
    Converts markdown-style text into a more natural format for Telegram,
    removing markdown symbols and ensuring appropriate spacing.
    """
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'\*\s', '- ', text)
    text = re.sub(r'(\d+)\.\s', r'\1) ', text)
    text = re.sub(r'##', '', text)
    text = re.sub(r'(\n\s*)\n', r'\1', text)
    text = re.sub(r'(^|\n)([^\n-])', r'\1\n\2', text)
    return text.strip()


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f"Hi, {message.from_user.first_name}!\nI am V4Fire assistant, I can help you to write components.\nAsk any question related to V4Fire :)")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    request = message.text
    response = get_response(request)
        
    bot.send_message(message.chat.id,
                     response,
                     parse_mode='Markdown'
                     )

def run_bot():
    while True:
        try:
            bot.polling(non_stop=True, interval=0)
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
