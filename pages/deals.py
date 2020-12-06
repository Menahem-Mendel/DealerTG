
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto, ParseMode
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler, Dispatcher, CallbackContext)


class DealsPage(controller.Page):
    entry = consts.DEALS

    photo = 'assets/img/deal.png'
    keyboard = []

    text = 'search page'

    def __init__(self):
        super().__init__({

        })

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
            with open(self.photo, 'rb') as photo:
                update.callback_query.edit_message_media(
                    media=InputMediaPhoto(photo),
                )  # send photo
            update.callback_query.edit_message_caption(
                caption=f'{self.text}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send text

            with open(self.photo, 'rb') as photo:
                update.callback_query.edit_message_media(
                    media=InputMediaPhoto(photo),
                )  # send photo
            update.callback_query.edit_message_caption(
                caption=f'{self.text}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send text

            update.callback_query.answer(
                text='fuck',
            )


Deals = DealsPage().handler
