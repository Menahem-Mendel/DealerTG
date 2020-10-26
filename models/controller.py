from collections import deque
from typing import Any

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler,
                          conversationhandler)

from models import consts, page

stack = deque()


class Controller:

    def __init__(self, controllers: list = []):
        self.controllers = controllers
        self.page = page.Page(self.controllers)
        self.handlers = [controller.conv() for controller in self.controllers]

    def handler(self, update: Update, context: CallbackContext):
        if update.callback_query:
            self.back_handler(update, context)

            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=self.page.text,
                reply_markup=self.page.markup(),
                parse_mode=telegram.ParseMode.HTML)

        elif update.message:
            if update.message.text:
                update.message.reply_text(
                    text=self.page.text,
                    reply_markup=self.page.markup(),
                    parse_mode=telegram.ParseMode.HTML)

        return self.entry

    def conv(self):
        return ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.handler),
                CallbackQueryHandler(self.handler, pattern=f'^{self.entry}$'),
            ],
            states={
                self.entry: self.handlers,
            },
            fallbacks=[
                CallbackQueryHandler(
                    self.handler, pattern=f'^{consts.BACK}{self.entry}$'),
                # CallbackQueryHandler(
                #     self.end, pattern=f'{consts.END}')
            ],
        )

    def back_handler(self, update: Update, context: CallbackContext):
        if update.callback_query.data is not f'{consts.BACK}{context.user_data.get(consts.BACK)}':
            # print(f'{stack}.append({context.user_data.get(consts.BACK)})')
            if context.user_data.get(consts.BACK):
                stack.append(context.user_data.get(consts.BACK))
                if self.entry is not consts.HOME:
                    self.page.back([
                        InlineKeyboardButton(
                            text=consts.BACK, callback_data=f'{consts.BACK}{context.user_data.get(consts.BACK)}')
                    ])
            # print(f'{context.user_data}.update({{{consts.BACK}: {self.entry}}})')
            context.user_data.update({consts.BACK: self.entry})
        else:
            context.user_data[consts.BACK] = stack.pop()
            update.callback_query.answer()

    def handle_func(self, pattern: str, handler):
        self.handlers.append(
            CallbackQueryHandler(handler, pattern=f'{pattern}'))
        self.page.add_btns([
            [InlineKeyboardButton(text=pattern, callback_data=pattern)]
        ])

        return
