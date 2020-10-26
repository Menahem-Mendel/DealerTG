from models import consts, controller, page
from telegram import Update
from telegram.ext import CallbackContext


class SearchPage(page.Page):
    def __init__(self, controllers: list = []):
        super().__init__(controllers)

    text = 'search page'


class SearchController(controller.Controller):
    entry = consts.SEARCH

    def __init__(self, controllers: list = []):
        super().__init__(controllers)
        self.page = SearchPage(self.controllers)
