
import i18n
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto, ParseMode
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler, Dispatcher, CallbackContext)

from database.DataBase import User


class DealsPage(controller.Page):
    entry = consts.DEALS
    photo = 'assets/img/deal.png'

    text = 'deals'

    def __init__(self):
        super().__init__(
            states={
                self.entry: [
                    ConversationHandler(
                        entry_points=[
                            CallbackQueryHandler(
                                self.add_deal, pattern=rf'{consts.ADD_DEAL}')
                        ],
                        states={
                            consts.EDIT_LOCATION: [MessageHandler(Filters.location, self.edit_location)],
                            consts.EDIT_DESCRIPTION: [MessageHandler(Filters.text, self.edit_description)],
                        },
                        fallbacks=[

                        ]
                    )
                ]
            }
        )

    def custom_handler(self, update: Update, context: CallbackContext):
        user = User(update.callback_query.from_user.id)

        self.keyboard = [
            [
                [
                    '+', consts.ADD_DEAL
                ]
            ]
        ]

        self.text = self.get_string(f'text.deals')

    def add_deal(self, update: Update, context: CallbackContext):
        self.keyboard = []

        self.text = self.get_string(f'text.edit_location')
        self.markup = self.build_keyboard()
        self.send_page(update, context)
        return consts.EDIT_LOCATION

    def edit_location(self, update: Update, context: CallbackContext):
        self.text = self.get_string(f'text.edit_description')
        self.send_page(update, context)  # reply to user sended message
        return consts.EDIT_DESCRIPTION

    def edit_description(self, update: Update, context: CallbackContext):
        self.text = self.get_string(f'text.edit_description')
        self.send_page(update, context)  # reply to user sended message
        return self.entry

    # def handler_func(self, update: Update, context: CallbackContext):
    #     context.user_data[consts.ADMIN] = False

    #     if context.user_data.get(consts.ADMIN):
    #         self.keyboard = [
    #             [
    #                 ['add_deal', consts.ADD_DEAL]
    #             ]
    #         ]

    #     context.user_data['lang'] = 'en'

    #     self.markup = self.build(lang=context.user_data.get('lang'))

    #     # if self.entry != consts.HOME and context.user_data.get(self.entry):
    #     #     self.markup = self.build(
    #     #         lang=context.user_data.get('lang'),
    #     #         btns=[
    #     #             [
    #     #                 [
    #     #                     'back',
    #     #                     context.user_data.get(self.entry)
    #     #                 ],
    #     #             ],
    #     #         ]
    #     #     )

    #     # context.user_data[self.entry] = self.entry
    #     self.back(update, context)

    #     self.reply(update, context)

    # def reply(self, update: Update, context: CallbackContext):
    #     i18n.load_path.append('i18n')
    #     if update.callback_query:

    #         with open(self.photo, 'rb') as photo:
    #             update.callback_query.edit_message_media(
    #                 media=InputMediaPhoto(photo),
    #             )  # send photo
    #             update.callback_query.edit_message_caption(
    #                 caption=i18n.t(
    #                     f'text.{self.text}',
    #                     vars={
    #                         'seller': 'mendel'
    #                     },
    #                     # seller='mendel',
    #                     # location='location',
    #                     # description='description',
    #                     locale=context.user_data.get('lang')
    #                 ),
    #                 reply_markup=InlineKeyboardMarkup(self.markup),
    #                 parse_mode=ParseMode.HTML,
    #             )  # send text

    #             update.callback_query.answer(
    #                 text='fuck',
    #             )
Deals = DealsPage().handler
