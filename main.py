
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, PicklePersistence, Updater)

from pages.home import Home

import config


def main():
    updater = Updater(config.token)
    dp = updater.dispatcher

    dp.add_handler(Home.build().conv())

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
