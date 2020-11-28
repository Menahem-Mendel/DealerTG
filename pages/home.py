from models import consts, controller, page
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler)


class HomePage(page.Page):
    def __init__(self, controllers: list = []):
        super().__init__(controllers)

    text = 'home page'


class HomeController(controller.Controller):
    entry = consts.HOME

    def __init__(self, controllers: list = []):
        super().__init__(controllers)
        self.page = HomePage(controllers)
        self.handle_func("like", "like", self.some_handler)

    def some_handler(self, update: Update, context: CallbackContext):
        if update.callback_query:
            update.callback_query.answer()
