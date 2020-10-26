from models import consts, controller, page
from telegram import Update
from telegram.ext import CallbackContext


class HomePage(page.Page):
    def __init__(self, controllers: list = []):
        super().__init__(controllers)

    text = 'home page'


class HomeController(controller.Controller):
    entry = consts.HOME

    def __init__(self, controllers: list = []):
        super().__init__(controllers)
        self.page = HomePage(self.controllers)
