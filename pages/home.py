
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class HomePage(controller.Page):
    entry = consts.HOME

    photo = 'assets/img/home.png'

    text = 'home'

    def __init__(self):
        super().__init__(
            states={

            },
            keyboard=[
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
        )


Home = HomePage().handler
