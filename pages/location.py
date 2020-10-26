from models import consts, controller, page
from telegram import Update
from telegram.ext import CallbackContext


class LocationPage(page.Page):
    def __init__(self, controllers: list = []):
        super().__init__(controllers)

    text = 'location page'


class LocationController(controller.Controller):
    entry = consts.LOCATION

    def __init__(self, controllers: list = []):
        super().__init__(controllers)
        self.page = LocationPage(self.controllers)

    # def handler(self, update: Update, context: CallbackContext):
    #     print('i was here')
    #     # context.user_data[consts.LOCATION] = update.message.location

    #     return self.back_handler(update, context)
