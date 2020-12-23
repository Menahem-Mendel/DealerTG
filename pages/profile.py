
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)
from database.DataBase import User


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

    def custom_handler(self, update: Update, context: CallbackContext):
        user = User(update.callback_query.from_user.id)

        self.text = self.text.format(
            name=user["name"],
            rating=user['rating'],
            language=user['language'],
            description=user['description'])

        self.tg_photo = user['photo']


Profile = ProfilePage().handler
