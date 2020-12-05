
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler, Dispatcher, CallbackContext)


class SearchPage(controller.Page):
    entry = consts.SEARCH
    keyboard = [
        [
            InlineKeyboardButton(text='filter 🔬', callback_data=consts.SEARCH)
        ],
        [
            InlineKeyboardButton(text='pick location 📍',
                                 callback_data=consts.LOCATION),
        ],
    ]
    text = 'search page'

    def __init__(self):
        super().__init__(ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    callback=self.handler_func, pattern=rf"^{self.entry}$")

            ],
            states={
                self.entry: [MessageHandler(Filters.text, self.search)]
            },
            fallbacks=[
            ]
        ))

    def search(self, update: Update, context: CallbackContext):
        if update.message:
            update.message.reply_photo(
                photo=open('assets/img/deal.png', 'rb'),
                caption=f'{update.message.text}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send photo with text
            update.message.reply_photo(
                photo=open('assets/img/deal.png', 'rb'),
                caption=f'{update.message.text}',
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send photo with text


Search = SearchPage().handler
