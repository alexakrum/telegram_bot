from dotenv import load_dotenv
import os
import telebot

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
