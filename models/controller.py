
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, Handler, MessageHandler)

from models import consts


class Page:
    photo = 'assets/img/home.png'
    keyboard = []
    text = 'base'
    entry = 'base'

    def __init__(self, states: dict = {}):
        self.states = states
        self.handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.handler_func) if self.entry == consts.HOME
                else CallbackQueryHandler(self.handler_func, pattern=rf"^{self.entry}$"),
            ],
            states=self.states,
            fallbacks=[
                CallbackQueryHandler(
                    self.back_handler, pattern=rf"^{self.entry}$")

            ]
        )

    def build(self, btns: list = []):
        m = []
        m.extend(self.keyboard)
        m.extend(btns)
        return m

    def handler_func(self, update: Update, context: CallbackContext):
        self.markup = self.keyboard

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

            # update.callback_query.message.delete()
            # with open(self.photo, 'rb') as photo:
            #     update.callback_query.message.reply_photo(
            #         photo=photo,
            #         caption=f'{self.text}',
            #         reply_markup=InlineKeyboardMarkup(self.markup),
            #         parse_mode=ParseMode.HTML,
            #     )  # send photo with text

            update.callback_query.answer(
                text='fuck',
            )

        elif update.message:
            update.message.delete()  # delete user command
            with open(self.photo, 'rb') as photo:
                update.message.reply_photo(
                    photo=photo,
                    caption=f'{self.text}',
                    reply_markup=InlineKeyboardMarkup(self.markup),
                    parse_mode=ParseMode.HTML,
                )  # send photo with text

        return self.entry

    def back(self, update: Update, context: CallbackContext):
        if self.entry != context.user_data.get(consts.BACK):
            context.user_data[self.entry +
                              consts.BACK] = context.user_data.get(consts.BACK)
            context.user_data[consts.BACK] = self.entry

        if context.user_data.get(self.entry+consts.BACK) and self.entry != consts.HOME:
            self.markup = self.build(
                [[InlineKeyboardButton(
                    text=consts.BACK, callback_data=context.user_data.get(self.entry+consts.BACK))]]
            )

    def back_handler(self, update: Update, context: CallbackContext):
        context.user_data[consts.BACK] = context.user_data.get(
            self.entry+consts.BACK)
        return self.handler_func(update, context)
