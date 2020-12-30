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
                            self.entry: self.entry,
                        }
                    )
                ]
            }
        )

        # !!!??? update id = update id + 1

    def custom_handler(self, update: Update, context: CallbackContext):
        # how to check if user is admin???

        # check for one deal
        # deal = Deal(...)
        # if deal.user.id == update.user.id

        user = User(update.callback_query.from_user.id)

        self.text = f'deals'
        self.keyboard = [
            [
                [
                    '+', consts.ADD_DEAL
                ]
            ]
        ]
        self.markup = self.build_keyboard()

    def add_deal(self, update: Update, context: CallbackContext):
        self.keyboard = []
        self.text = f'ask_location'

        self.markup = self.build_keyboard()
        self.send_page(update, context)
        return consts.EDIT_LOCATION

    def ask_location(self, update: Update, context: CallbackContext):

        self.text = f'ask_description'
        self.keyboard = [
            [
                [
                    'cancel', consts.CANCEL
                ]
            ]
        ]

        self.markup = self.build_keyboard()
        self.send_page(update, context)
        return consts.EDIT_DESCRIPTION

    def ask_description(self, update: Update, context: CallbackContext):
        self.text = f'deals'
        self.keyboard = [
            [
                [
                    '+', consts.ADD_DEAL
                ]
            ]
        ]

        self.markup = self.build_keyboard()
        self.send_page(update, context)
        return self.entry


Deals = DealsPage().handler
