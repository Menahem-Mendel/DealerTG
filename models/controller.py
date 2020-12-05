
from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup, ParseMode, InputMediaPhoto, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, Handler, MessageHandler,)

from models import consts, page


class Controller:
    def __init__(self, handler):
        self.handler = handler
        self.page = page.Page()

    def handler_func(self, update: Update, context: CallbackContext):
        self.markup = self.page.keyboard

        self.back(update, context)

        if update.callback_query:
            # update.callback_query.edit_message_media(
            #     media=InputMediaPhoto(open('assets/img/deal.png', 'rb')),
            # )  # send photo
            # update.callback_query.edit_message_caption(
            #     caption=f'{self.entry}',
            #     reply_markup=InlineKeyboardMarkup(self.markup),
            #     parse_mode=ParseMode.HTML,
            # )  # send text

            update.callback_query.message.reply_photo(
                photo=open('assets/img/deal.png', 'rb'),
                caption=f'{self.entry}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send photo with text

            update.callback_query.answer(
                text='fuck',
            )

        elif update.message:
            update.message.delete()  # delete user command
            update.message.reply_photo(
                photo=open('assets/img/deal.png', 'rb'),
                caption=f'{self.entry}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send photo with text

        return self.entry

    def back(self, update: Update, context: CallbackContext):
        if not context.user_data.get(consts.BACK):
            context.user_data[consts.BACK] = []

        if len(context.user_data.get(consts.BACK)) > 0 and self.entry != consts.HOME:

            if self.entry != consts.HOME:
                self.markup = self.page.markup([
                    [InlineKeyboardButton(
                        text=consts.BACK, callback_data=context.user_data.get(consts.BACK)[-1])]
                ])

        print(context.user_data.get(consts.BACK))
        if len(context.user_data.get(consts.BACK)) > 1:
            print('1')
            if context.user_data.get(consts.BACK)[-2] == self.entry:
                context.user_data[consts.BACK].pop()
                return

        context.user_data[consts.BACK].append(self.entry)
