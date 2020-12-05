
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, Handler, MessageHandler)

from models import consts


class Page:
    photo = None
    keyboard = []
    text = ''

    def __init__(self, handler):
        self.handler = handler

    def build(self, btns: list = []):
        m = []
        m.extend(self.keyboard)
        m.extend(btns)
        return m

    def handler_func(self, update: Update, context: CallbackContext):
        self.markup = self.keyboard

        self.back(update, context)

        if update.callback_query:
            update.callback_query.edit_message_media(
                media=InputMediaPhoto(open('assets/img/deal.png', 'rb')),
            )  # send photo
            update.callback_query.edit_message_caption(
                caption=f'{self.text}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send text

            # update.callback_query.message.reply_photo(
            #     photo=open('assets/img/deal.png', 'rb'),
            #     caption=f'{self.entry}',
            #     reply_markup=InlineKeyboardMarkup(self.markup),
            #     parse_mode=ParseMode.HTML,
            # )  # send photo with text

            update.callback_query.answer(
                text='fuck',
            )

        elif update.message:
            update.message.delete()  # delete user command
            update.message.reply_photo(
                photo=open('assets/img/deal.png', 'rb'),
                caption=f'{self.text}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send photo with text

    def back(self, update: Update, context: CallbackContext):
        if self.entry != context.user_data.get(consts.BACK):
            context.user_data[self.entry] = context.user_data.get(consts.BACK)
            context.user_data[consts.BACK] = self.entry
        else:
            context.user_data[consts.BACK] = context.user_data.get(self.entry)

        if context.user_data.get(self.entry) and self.entry != consts.HOME:
            self.markup = self.build(
                [[InlineKeyboardButton(
                    text=consts.BACK, callback_data=context.user_data.get(self.entry))]]
            )
