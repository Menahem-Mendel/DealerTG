
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, PicklePersistence, Updater)

from pages import deals, home, location, search


def main():
    pp = PicklePersistence(filename='state')
    updater = Updater("1212727091:AAFcRS0ZON0CBP0dntrgZy7IZwxZd40AAFM",
                      persistence=pp)
    dp = updater.dispatcher

    conv = home.HomeController([
        search.SearchController(),
        deals.DealsController([
            location.LocationController(),
        ])
    ]).conv()

    dp.add_handler(conv)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
