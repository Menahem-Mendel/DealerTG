
import i18n
from models import consts, controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto, ParseMode
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, conversationhandler, Dispatcher, CallbackContext)


class DealsPage(controller.Page):
    entry = consts.DEALS
    photo = 'assets/img/deal.png'

    text = 'deals'

    def __init__(self):
        super().__init__(
            states={

            },
            keyboard=[
                [
                    ['bookmark', consts.ADD_BOOKMARK]
                ],
                [
                    ['profile', consts.PROFILE],
                    ['chat', consts.TOCHAT],
                ],
                [
                    ['order', consts.ORDER]
                ],
            ]
        )

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
