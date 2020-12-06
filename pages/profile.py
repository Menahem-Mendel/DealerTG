
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class ProfilePage(controller.Page):
    entry = consts.PROFILE

    photo = 'assets/img/profile.png'

    keyboard = [
        [
            InlineKeyboardButton(text='deals 💼',
                                 callback_data=consts.DEALS)
        ],
        [
            InlineKeyboardButton(text='comments 💬',
                                 callback_data=consts.COMMENTS),
        ],
        [
            InlineKeyboardButton(text='rogue ⚠️',
                                 callback_data=consts.HELP),
        ],
        [
            InlineKeyboardButton(text='like ❤️',
                                 callback_data=consts.LIKE),
            InlineKeyboardButton(text='dislike 💔',
                                 callback_data=consts.DISLIKE),
        ],
    ]

    text = 'search page'

    def __init__(self):
        super().__init__({

        })


Profile = ProfilePage().handler
