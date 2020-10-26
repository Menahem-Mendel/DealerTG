from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from models import consts


class Page:

    def __init__(self, controllers: list = []):
        self.controllers = controllers
        self.btns = [
            [InlineKeyboardButton(text=controller.entry, callback_data=controller.entry)] for controller in self.controllers
        ]

    def markup(self):
        return InlineKeyboardMarkup(
            self.btns
        )

    def add_btns(self, btns):
        self.btns.extend(btns)

    has = False

    def back(self, btn):
        if not self.has:
            self.btns.append(btn)
            self.has = True
            return

        self.btns[-1] = btn

    text = 'default page'
