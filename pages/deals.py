import pages.location
from models import consts, controller, page
from telegram import Update
from telegram.ext import CallbackContext


class DealsPage(page.Page):
    def __init__(self, controllers: list = []):
        super().__init__(controllers)

    text = 'deals page'


class DealsController(controller.Controller):
    entry = consts.DEALS

    def __init__(self, controllers: list = []):
        super().__init__(controllers)
        self.page = DealsPage(controllers)

    def build(self):
        return DealsController([
            pages.location.LocationController(),
        ])
