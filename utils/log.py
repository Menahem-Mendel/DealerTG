import telegram
import logging
import os


def setup_logger(name, level=logging.INFO):
    if not os.path.exists('log'):
        os.makedirs('log')

    handler = logging.FileHandler(os.path.join('log', name + '.log'))
    handler.setFormatter(formatter)

    logger = logging.getLogger(name + 'Dealer')
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

infoLogger = setup_logger('info', level=logging.INFO)
errorLogger = setup_logger('error', level=logging.ERROR)
actionLogger = setup_logger('action', level=logging.DEBUG)


class TgLog:

    def info(text):
        infoLogger.info(text)

        TgLog.__send('info - ' + text)

    def error(text):
        errorLogger.error(text)

        TgLog.__send('error - ' + text)

    def action(text):
        actionLogger.debug(text)

        TgLog.__send('action - ' + text)

    def __send(text):
        bot = telegram.Bot('1237744951:AAHZFIaqis0hEul3b46NDzrgZCoeP2Lz4Xw')
        chat_id = bot.get_updates()[-1].message.chat_id
        bot.send_message(chat_id=chat_id, text=text)
