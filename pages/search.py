import telegram
from models import consts, controller, page
from telegram import InlineKeyboardButton, Update
from telegram.ext import CallbackContext, Filters, MessageHandler

import pages.deals


class SearchPage(page.Page):
    def __init__(self, controllers: list = []):
        super().__init__(controllers)

    text = 'search page'


class SearchController(controller.Controller):
    entry = consts.SEARCH

    def __init__(self, controllers: list = []):
        super().__init__(controllers)
        self.page = SearchPage(controllers)
    #     self.states[self.entry].append(MessageHandler(
    #         Filters.text, callback=self.results)
    #     )

    # def results(self, update: Update, context: CallbackContext):
    #     results = [
    #         {
    #             'photo': "https://www.w3schools.com/images/w3schools_green.jpg",
    #             'page': pages.deals.DealsController(),
    #         },
    #         {
    #             'photo': "https://www.w3schools.com/images/w3schools_green.jpg",
    #             'page': pages.deals.DealsController(),
    #         }
    #     ]

    #     # if update.callback_query:
    #     #     if update.callback_query.data ==
    #     if update.message:
    #         if update.message.text:
    #             for result in results:
    #                 update.message.reply_photo(
    #                     photo=result.get('photo'),
    #                     parse_mode=telegram.ParseMode.HTML
    #                 )
    #                 update.message.reply_text(
    #                     text=result.get('text'),
    #                     reply_markup=result.get('page').markup(),
    #                     parse_mode=telegram.ParseMode.HTML
    #                 )
