from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Page:
    photo = None
    keyboard = []
    text = ''

    def markup(self, btns: list = []):
        m = []
        m.extend(self.keyboard)
        m.extend(btns)
        return m
