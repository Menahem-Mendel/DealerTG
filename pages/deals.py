from database.DataBase import User
from models import consts, controller
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, MessageHandler, conversationhandler)


class DealsPage(controller.Page):
    entry: str = consts.DEALS
    photo: str = 'assets/img/deal.png'
    text: str = 'deals'
    keyboard: list = []

    def __init__(self):
        super().__init__(
            states={
                self.entry: [
                    ConversationHandler(
                        entry_points=[
                            MessageHandler(Filters.text, self.ask_description)
                        ],
                        states={
                            consts.EDIT_LOCATION: [MessageHandler(Filters.location, self.ask_location)],
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
        return consts.EDIT_LOCATION

    def ask_description(self, update: Update, context: CallbackContext):
        self.keyboard = []
        self.text = f'text.ask_description'
        self.send_page(update, context)  # reply to user sended message
        return consts.EDIT_LOCATION

    def ask_location(self, update: Update, context: CallbackContext):
        self.text = f'text.ask_location'
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
