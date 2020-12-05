
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto, ParseMode
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler, Dispatcher, CallbackContext)


class DealsPage(controller.Page):
    entry = consts.DEALS

    photo = open('assets/img/deal.png', 'rb')
    keyboard = []

    text = 'search page'

    def __init__(self):
        super().__init__(ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    callback=self.handler_func, pattern=rf"^{self.entry}$")
            ],
            states={
                consts.USER: [

                ],
                consts.ADMIN: [

                ],
            },
            fallbacks=[

            ]
        ))

    def handler_func(self, update: Update, context: CallbackContext):
        self.keyboard = [
            [
                InlineKeyboardButton(text='+', callback_data=consts.SEARCH)
            ],
        ]

        self.markup = self.keyboard

        self.markup = self.build([
            [
                InlineKeyboardButton(text='+', callback_data=consts.DEALS)
            ]
        ])

        self.back(update, context)

        if update.callback_query:

            update.callback_query.message.reply_photo(
                photo=open('assets/img/deal.png', 'rb'),
                caption=f'{self.entry}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send photo with text
            update.callback_query.message.reply_photo(
                photo=open('assets/img/deal.png', 'rb'),
                caption=f'{self.entry}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send photo with text

            update.callback_query.answer(
                text='fuck',
            )


Deals = DealsPage().handler
