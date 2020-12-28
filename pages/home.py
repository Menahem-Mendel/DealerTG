from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class HomePage(controller.Page):
    entry: str = consts.HOME
    photo: str = 'assets/img/home.png'
    text: str = 'home'
    keyboard: list = [
        [
            ['search', consts.SEARCH]
        ],
        [
            ['deals', consts.DEALS],
            ['profile', consts.PROFILE],
        ],
        [
            ['bookmarks', consts.BOOKMARKS],
        ],
        [
            ['help', consts.HELP],
            ['info', consts.INFO],
        ],
    ]

    def __init__(self):
        super().__init__(
            states={

            }
        )


Home = HomePage().handler
