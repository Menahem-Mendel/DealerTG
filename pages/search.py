

import telegram
from models import consts, controller, page
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Filters, MessageHandler

import pages.deals
import pages.location


class SearchPage(page.Page):
    def __init__(self, controllers: list = []):
        super().__init__(controllers)

    text = 'search page'


class SearchController(controller.Controller):
    entry = consts.SEARCH

    def __init__(self, controllers: list = []):
        super().__init__(controllers)
        self.page = SearchPage(controllers)
        self.handle_func(MessageHandler(Filters.text, callback=self.results))

    def build(self):
        return SearchController([
            pages.location.LocationController(),
        ])

    def results(self, update: Update, context: CallbackContext):
        # self.handle_func(pages.deals.DealsController(), 'something')
        update.message.reply_text(
            text=self.page.text,
            reply_markup=self.markup
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(text=pages.deals.DealsController().build(
            ).entry, callbackdata=pages.deals.DealsController().build().entry)]
        ])
        update.message.reply_text(
            text='one',
            reply_markup=markup
        )
        update.message.reply_text(
            text='two',
            reply_markup=markup
        )
