from collections import deque
from re import match

import telegram
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      replymarkup)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler,
                          conversationhandler)

from models import consts, page

stack = deque()


class Controller:
    def __init__(self, controllers: list = []):
        self.controllers = controllers
        self.handlers = [controller.conv() for controller in self.controllers]
        self.state = self.entry
        self.page = page.Page(controllers=self.controllers)

    def init(self, controllers: list = []):
        self.controllers = controllers
        self.handlers = [controller.conv() for controller in self.controllers]
        self.page = page.Page(controllers=self.controllers)
        return self

    def back(self, update: Update, context: CallbackContext):
        if len(context.user_data.get(consts.BACK)) > 1 and update.callback_query.data == context.user_data.get(consts.BACK)[-2]:
            context.user_data[consts.BACK].pop()
            context.user_data[consts.BACK].pop()

        return self.handler(update, context)

    def handler(self, update: Update, context: CallbackContext):
        markup = self.page.markup()

        if not context.user_data.get(consts.BACK):
            context.user_data.update({consts.BACK: []})
            context.user_data[consts.BACK].append(f'{self.entry}')

        if update.callback_query:
            if update.callback_query.data == consts.HOME:
                context.user_data.update({consts.BACK: []})
            else:
                markup = self.page.markup([[
                    InlineKeyboardButton(
                        text=consts.BACK, callback_data=f'{context.user_data.get(consts.BACK)[-1]}')
                ]])

            context.user_data[consts.BACK].append(f'{self.entry}')

            update.callback_query.edit_message_text(
                text=self.page.text,
                reply_markup=markup,
                parse_mode=telegram.ParseMode.HTML)

            update.callback_query.answer()

        elif update.message:
            if update.message.text:
                update.message.reply_text(
                    text=self.page.text,
                    reply_markup=markup,
                    parse_mode=telegram.ParseMode.HTML)

        return self.state

    def conv(self):
        return ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.handler),
                CallbackQueryHandler(self.handler, pattern=f'^{self.entry}$'),
            ],
            states={
                self.state: self.handlers,
            },
            fallbacks=[
                CallbackQueryHandler(
                    self.back, pattern=f'^{self.entry}$'),
            ],
        )
