
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class HomePage(controller.Page):
    entry = consts.HOME

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
        super().__init__(ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.handler_func),
                CallbackQueryHandler(
                    callback=self.handler_func, pattern=rf"^{self.entry}$")

            ],
            states={
                self.entry: [

                ]
            },
            fallbacks=[
            ]
        ))


Home = HomePage().handler
