
from telegram.ext import Updater

from pages import deals, home, search, location


def main():
    updater = Updater(token="1212727091:AAFcRS0ZON0CBP0dntrgZy7IZwxZd40AAFM")
    dp = updater.dispatcher

    l = location.LocationController()
    s = search.SearchController([
        l,
    ])
    d = deals.DealsController([
        l,
        s,
    ])
    conv = home.HomeController([
        s,
        d,
    ]).conv()

    dp.add_handler(conv)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
