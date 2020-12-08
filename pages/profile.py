
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class ProfilePage(controller.Page):
    entry = consts.PROFILE

    photo = 'assets/img/profile.png'

    text = 'profile'

    def __init__(self):
        super().__init__(
            states={

            },
            keyboard=[
                [
                    ['deals', consts.DEALS]
                ],
                [
                    ['comments', consts.COMMENTS],
                ],
                [
                    ['rogue', consts.HELP],
                ],
                [
                    ['like', consts.LIKE],
                    ['dislike', consts.DISLIKE],
                ],
            ]
        )


Profile = ProfilePage().handler
