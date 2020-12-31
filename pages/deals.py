from database.DataBase import User
from models import consts, controller
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class DealsPage(controller.Page):
    # defalult values
    entry: str = consts.DEALS
    photo: str = 'assets/img/deal.png'
    text: str = 'deals'
    keyboard: list = []

    def __init__(self):
        super().__init__(
            states={
                self.entry: [
                    ConversationHandler(
                        entry_points=[
                            CallbackQueryHandler(
                                self.add_deal, rf'{consts.ADD_DEAL}')
                        ],
                        states={
                            consts.EDIT_LOCATION: [MessageHandler(Filters.location, self.ask_location)],
                            consts.EDIT_DESCRIPTION: [MessageHandler(Filters.text, self.ask_description)],
                        },
                        fallbacks=[

                        ],
                        map_to_parent={
                            consts.END: self.entry,
                        }
                    ),
                ],
            }
        )

    def custom_handler(self, update: Update, context: CallbackContext):
        context.user_data.update(
            {
                consts.TEXT: self.entry,
                consts.KEYBOARD: [
                    [
                        [
                            '+', consts.ADD_DEAL
                        ]
                    ]
                ]
            }
        )

    def add_deal(self, update: Update, context: CallbackContext):
        context.user_data.update(
            {
                consts.TEXT: f'ask_location',
                consts.KEYBOARD: []
            }
        )

        self.send_page(update, context)
        return consts.EDIT_LOCATION

    def ask_location(self, update: Update, context: CallbackContext):
        context.user_data.update(
            {
                consts.TEXT: f'ask_description',
                consts.KEYBOARD: [
                    [
                        [
                            'cancel', consts.CANCEL
                        ]
                    ]
                ]
            }
        )

        self.send_page(update, context)
        return consts.EDIT_DESCRIPTION

    def ask_description(self, update: Update, context: CallbackContext):
        context.user_data.update(
            {
                consts.TEXT: self.text,
                consts.KEYBOARD: [
                    [
                        [
                            '+', consts.ADD_DEAL
                        ]
                    ]
                ]
            }
        )

        self.send_page(update, context)
        return consts.END


Deals = DealsPage().handler
