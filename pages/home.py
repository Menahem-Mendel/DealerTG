
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class HomePage(controller.Page):
    entry = consts.HOME

    photo = 'assets/img/home.png'

    keyboard = [
        [
            InlineKeyboardButton(text='search 🔎', callback_data=consts.SEARCH)
        ],
        [
            InlineKeyboardButton(text='deals 💼', callback_data=consts.DEALS),
            InlineKeyboardButton(
                text='profile 👨‍', callback_data=consts.PROFILE),
        ],
        [
            InlineKeyboardButton(
                text='bookmarks 📑', callback_data=consts.BOOKMARKS)
        ],
        [
            InlineKeyboardButton(text='help 💬', callback_data=consts.HELP),
            InlineKeyboardButton(text='info ℹ️', callback_data=consts.INFO),
        ],
    ]

    text = 'home page'

    def __init__(self):
        super().__init__({

        })


Home = HomePage().handler
