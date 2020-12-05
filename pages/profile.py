
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class ProfilePage(controller.Page):
    entry = consts.PROFILE
    keyboard = [
        [
            InlineKeyboardButton(text='filter', callback_data=consts.FILTER)
        ],
        [
            InlineKeyboardButton(text='pick location',
                                 callback_data=consts.LOCATION),
        ],
    ]

    text = 'search page'

    def __init__(self):
        super().__init__(ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    callback=self.handler_func, pattern=rf"^{self.entry}$")
            ],
            states={
            },
            fallbacks=[
            ]
        ))


Profile = ProfilePage().handler
