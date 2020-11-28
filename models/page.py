from models import controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from models import consts


class Page:
    def __init__(self, controllers: list = []):
        self.controllers = controllers
        self.btns = [
            [InlineKeyboardButton(text=controller.entry, callback_data=controller.entry)] for controller in self.controllers
        ]

    def append(self, btn: list = []):
        self.btns.append(btn)

    def markup(self, btns: list = []):
        keyboard = []
        keyboard.extend(self.btns)
        keyboard.extend(btns)

        return InlineKeyboardMarkup(
            keyboard
        )

    text = 'default page'
