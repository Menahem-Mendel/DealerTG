import pages.location
import pages.search
import pages.deals
from models import consts, controller, page
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler)


class ProfilePage(page.Page):
    def __init__(self, controllers: list = []):
        super().__init__(controllers)

    text = 'genious'


class ProfileController(controller.Controller):
    entry = 'profile'

    def __init__(self, controllers: list = []):
        super().__init__(controllers)

        self.page = ProfilePage(controllers)
        self.extend([pages.location.LocationController(),
                     pages.search.SearchController()])

        self.extend([pages.deals.DealsController()])
		# self.extend([])

        # self.handle_func([CallbackQueryHandler(
        #     callback=self.some, pattern='some')])
		# self.state[self.entry].append()


		
    def some(self):
        pass

    def build(self):
        return ProfileController([
            pages.deals.DealsController(),
        ])


Profile = ProfileController()
