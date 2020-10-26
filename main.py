
from telegram.ext import Updater

from pages import deals, home, search, location


def main():
    updater = Updater(token="1212727091:AAFcRS0ZON0CBP0dntrgZy7IZwxZd40AAFM")
    dp = updater.dispatcher

    conv = home.HomeController([
        search.SearchController(),
        deals.DealsController([
            location.LocationController()
        ]),
    ]).conv()

    dp.add_handler(conv)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
