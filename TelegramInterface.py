# https://github.com/python-telegram-bot/python-telegram-bot

import telegram
import logging
from telegram.ext import Updater

BOT_TOKEN = '1106057306:AAHzghsz0JEjov3imNpRzSaG-Z9kmWPqkQE'
bot = telegram.Bot(token=BOT_TOKEN)

LOGGING_CHAT = '390255012'
PLEX_USER_CHAT =''

def logToTelegram(text):
    bot.send_message(chat_id=LOGGING_CHAT, text=text)

def notifyPlexUsers(torrent_name, mediaFormat):
    bot.send_message(chat_id=PLEX_USER_CHAT, text="***New " + mediaFormat + " added: " + torrent_name)


