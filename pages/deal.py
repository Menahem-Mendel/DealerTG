from models import consts, controller
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class DealPage(controller.Page):
    entry: str = consts.DEAL
    photo: str = 'assets/img/deal.png'
    text: str = 'deal'
    keyboard: list = []

    def __init__(self):
        super().__init__(
            states={
            }
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
