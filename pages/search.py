
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto, ParseMode
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler, Dispatcher, CallbackContext)


class SearchPage(controller.Page):
    entry = consts.SEARCH

    photo = 'assets/img/search.png'

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
        super().__init__({
            self.entry: [
                CallbackQueryHandler(
                    callback=self.location, pattern=rf"^{consts.LOCATION}$")
            ],
            consts.LOCATION: [
                MessageHandler(Filters.location, self.location)
            ]
        })

    def location(self, update: Update, context: CallbackContext):
        if update.callback_query:
            update.callback_query.message.reply_text(
                text=f'send me location',
                parse_mode=ParseMode.HTML,
            )  # send text

            update.callback_query.answer(
                text='fuck',
            )

            return consts.LOCATION
        if update.message:
            update.message.delete()
            print(update.message.location)
            return self.entry


Search = SearchPage().handler
