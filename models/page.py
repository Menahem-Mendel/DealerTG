from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Page:
    # Page is a markup for page, but without any logic
    # it is better to use it with by Controller

    def __init__(self, controllers: list = []):
        self.btns = [
            [InlineKeyboardButton(text=controller.entry, callback_data=controller.entry)] for controller in controllers
        ]
        self.back = []

    def build(self, controllers: list = []):
        self.btns.append([
            InlineKeyboardButton(text=controller.entry, callback_data=controller.entry) for controller in controllers
        ])

    def append(self, btn: list = []):
        # append - adds buttons to our page one's and for all so you cannot remove it

        self.btns.extend(btn)

    def back_func(self, btn: list = []):
        self.back = btn

    def markup(self, btns: list = []):
        # markup - builds the inline keyboard structure

        keyboard = []
        keyboard.extend(self.btns)
        keyboard.extend(btns)
        keyboard.extend(self.back)

        return InlineKeyboardMarkup(
            keyboard
        )

    text = 'default page'
