from models import consts, controller
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class SearchPage(controller.Page):
    entry: str = consts.SEARCH
    photo: str = 'assets/img/search.png'
    text: str = 'search'
    keyboard: list = [
        [
            ['filter', consts.FILTER]
        ],
        [
            ['location', consts.LOCATION],
        ],
    ]

    def __init__(self):
        super().__init__(
            states={
                self.entry: [
                    CallbackQueryHandler(
                        callback=self.location, pattern=rf"^{consts.LOCATION}$")
                ],
                consts.LOCATION: [
                    MessageHandler(Filters.location, self.location)
                ]
            }
        )

    def location(self, update: Update, context: CallbackContext):
        if update.callback_query:
            self.text = "ask_for_location"
            self.send_page(update, context)

            update.callback_query.answer(
                text='fuck',
            )

            return consts.LOCATION
        if update.message:
            print(update.message.location)
            self.text = self.defult_text
            self.send_page(update, context)
            return self.entry


Search = SearchPage().handler
