import telegram
import logging
from decouple import config


def send_notification(message):
    bot = telegram.Bot(config('BOT_TOKEN'))
    try:
        bot.send_message(config('GROUP_ID'), message)
        logging.info("Message sent successfully")
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    send_notification(None)
