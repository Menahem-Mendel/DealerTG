import pages.profile
import pages.search
import pages.deals
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

    def build(self):
        return HomeController([
            pages.search.SearchController(),
            pages.deals.DealsController(),
            pages.profile.ProfileController(),
        ])


Home = HomeController()
