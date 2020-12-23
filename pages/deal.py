
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto, ParseMode
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler, Dispatcher, CallbackContext)


class DealPage(controller.Page):
    entry = consts.DEAL
    photo = 'assets/img/deal.png'

    text = 'deal'

    def __init__(self):
        super().__init__(
            states={
            },
            keyboard=[
            ]
        )

    def custem_handle(self, update: Update, context: CallbackContext):
        if context.user_data.get('admin') == True:
            self.keyboard = [
                [
                    ['search', consts.SEARCH]
                ],
            ]
        else:
            self.keyboard = [
                [
                    ['search', consts.SEARCH]
                ],
            ]

            self.markup = self.build_keyboard()


Deal = DealPage().handler
