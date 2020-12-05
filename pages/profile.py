
from models import consts, controller, page
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class ProfilePage(page.Page):
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


class ProfileController(controller.Controller):
    entry = consts.PROFILE

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
        self.page = ProfilePage()


Profile = ProfileController().handler
