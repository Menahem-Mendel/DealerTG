
from models import consts, controller, page
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto, ParseMode
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler, Dispatcher, CallbackContext)


class DealsPage(page.Page):
    photo = open('assets/img/deal.png', 'rb')
    keyboard = []

    text = 'search page'


class DealsController(controller.Controller):
    entry = consts.DEALS

    def __init__(self):
        super().__init__(ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    callback=self.handler_func, pattern=rf"^{self.entry}$")
            ],
            states={
                consts.USER: [

                ],
                consts.ADMIN: [

                ],
            },
            fallbacks=[

            ]
        ))
        self.page = DealsPage()

    # def handler_func(self, update: Update, context: CallbackContext):
    #     self.page.keyboard = [
    #         [
    #             InlineKeyboardButton(text='+', callback_data=consts.SEARCH)
    #         ],
    #     ]

    #     self.markup = self.page.keyboard

    #     self.markup = self.page.markup([
    #         [
    #             InlineKeyboardButton(text='+', callback_data=consts.DEALS)
    #         ]
    #     ])

    #     self.back(update, context)

    #     if update.callback_query:
    #         update.callback_query.edit_message_media(
    #             media=InputMediaPhoto(open('assets/img/help.png', 'rb')),
    #         )  # send photo
    #         update.callback_query.edit_message_caption(
    #             caption=f'{self.entry}',
    #             reply_markup=InlineKeyboardMarkup(self.markup),
    #             parse_mode=ParseMode.HTML,
    #         )  # send text

    #         update.callback_query.edit_message_media(
    #             media=InputMediaPhoto(open('assets/img/help.png', 'rb')),
    #         )  # send photo
    #         update.callback_query.edit_message_caption(
    #             caption=f'{self.entry}',
    #             reply_markup=InlineKeyboardMarkup(self.markup),
    #             parse_mode=ParseMode.HTML,
    #         )  # send text

    #         update.callback_query.answer(
    #             text='fuck',
    #         )


Deals = DealsController().handler
