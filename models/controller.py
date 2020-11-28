
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, MessageHandler, Filters)

from models import consts, page


class Controller:
    def __init__(self, controllers: list = []):
        self.page = page.Page(controllers)
        self.markup = self.page.markup()
        self.states = {
            self.entry: [controller.conv() for controller in controllers]
        }

    def handler(self, update: Update, context: CallbackContext):
        if update.callback_query:
            update.callback_query.edit_message_text(
                text=self.page.text,
                reply_markup=self.markup,
                parse_mode=telegram.ParseMode.HTML
            )
            update.callback_query.answer()
        elif update.message:
            if not context.user_data.get(update.message.from_user.id):
                context.user_data.update({update.message.from_user.id: True})
            if update.message.text:
                update.message.reply_text(
                    text=self.page.text,
                    reply_markup=self.markup,
                    parse_mode=telegram.ParseMode.HTML
                )

        self.back(update, context)

        return self.entry

    def conv(self):
        return ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.handler),
                CallbackQueryHandler(self.handler, pattern=f'^{self.entry}$'),
            ],
            states=self.states,
            fallbacks=[
                CallbackQueryHandler(
                    self.handler, pattern=f'^{self.entry}$'),
            ],
            name=f'{self.entry}_conv',
            persistent=True,
            allow_reentry=True if self.entry == consts.HOME else False,
        )

    # def back_handler(self, update: Update, context: CallbackContext):
    #     if len(context.user_data.get(consts.BACK)) > 1 and update.callback_query.data == context.user_data.get(consts.BACK)[-2]:
    #         context.user_data[consts.BACK].pop()
    #         context.user_data[consts.BACK].pop()

    #     return self.handler(update, context)

    # def __push_back(self, update: Update, context: CallbackContext):
    #     if not context.user_data.get(consts.BACK):
    #         context.user_data.update({consts.BACK: []})
    #         context.user_data[consts.BACK].append(f'{self.entry}')
    #     if update.callback_query:
    #         if update.callback_query.data == consts.HOME:
    #             context.user_data.update({consts.BACK: []})
    #         else:
    #             self.markup = self.page.markup([
    #                 [InlineKeyboardButton(
    #                     text=consts.BACK, callback_data=f'{context.user_data.get(consts.BACK)[-1]}')]
    #             ])

    #         context.user_data[consts.BACK].append(f'{self.entry}')

    def back(self, update: Update, context: CallbackContext):
        if not context.user_data.get(self.entry):
            print('context(consts.BACK)', context.user_data.get(consts.BACK))
            print('context(self.entry)', context.user_data.get(self.entry))
            print('self.entry', self.entry)
            print()
            context.user_data.update({
                self.entry: context.user_data.get(consts.BACK)
            })
            context.user_data.update({
                consts.BACK: self.entry
            })

        if self.entry != consts.HOME:
            self.markup = self.page.markup([
                [InlineKeyboardButton(
                    text=consts.BACK, callback_data=f'{context.user_data.get(self.entry)}')]
            ])

    def handle_func(self, text: str, pattern: str, handler):
        self.states[self.entry].append(
            CallbackQueryHandler(handler, pattern=f'^{pattern}$')
        )
        self.page.append(
            [InlineKeyboardButton(text=text, callback_data=pattern)]
        )
        self.markup = self.page.markup()
