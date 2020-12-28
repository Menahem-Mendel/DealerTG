from database.DataBase import User
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class ProfilePage(controller.Page):
    entry: str = consts.PROFILE
    photo: str = 'assets/img/profile.png'
    text: str = 'profile'
    keyboard: list = [
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

    def __init__(self):
        super().__init__(
            states={

            }
        )

    def custom_handler(self, update: Update, context: CallbackContext):
        user = User(update.callback_query.from_user.id)

        context.user_data.update(
            {
                consts.TEXT_VARS: {
                    'name': user.get('name'),
                    'rating': user.get('rating'),
                    'language': user.get('language'),
                    'description': user.get('description')
                }
            }
        )

        self.tg_photo = user['photo']  # !!!


Profile = ProfilePage().handler
