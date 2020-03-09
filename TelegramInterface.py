import secrets
import telegram

LOG_BOT_TOKEN = secrets.LOG_BOT_TOKEN
PLEX_USER_BOT_TOKEN = secrets.PLEX_USER_BOT_TOKEN

logBot = telegram.Bot(token=LOG_BOT_TOKEN)
plexUserBot = telegram.Bot(token=PLEX_USER_BOT_TOKEN)

LOGGING_CHAT = secrets.LOGGING_CHAT
PLEX_USER_CHAT = secrets.PLEX_USER_CHAT

def logToTelegram(text):
    logBot.send_message(chat_id=LOGGING_CHAT, text=text)

def notifyPlexUsers(torrent_name, mediaFormat):
    try:
        plexUserBot.send_message(chat_id=PLEX_USER_CHAT, text="New " + mediaFormat + " added: \n'" + torrent_name + "'")
    except telegram.error.TimedOut as e:
        logBot.send_message(chat_id=LOGGING_CHAT, text="ERROR SENDING TO PLEX USERS: \n'" + e + "'")

