import i18n
import telegram
from database.DataBase import User
from telegram import (Chat, InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, Handler, MessageHandler)

from models import consts


class Page:
    tg_photo: str = None
    photo: str = None  # e.g. 'assets/img/deal.png'
    entry: str = None  # e.g. home
    text: str = None  # e.g. ask_location
    keyboard: list = []  # e.g. [[[text_id, callback]]]

    def __init__(self, states: dict = {}):
        self.handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.main_handler) if self.entry == consts.HOME
                else CallbackQueryHandler(self.main_handler, pattern=rf"^{self.entry}$"),
            ],  # entry_points sepcifies the entry handlers
            states=states,  # states is a conversation branches, for example if user pressed button it activates the returned state, and only few of callbacks can be processed
            fallbacks=[
                CallbackQueryHandler(
                    self.main_handler, pattern=rf"^{self.entry}$"),

            ],  # if you want to back to main state then specify this handlers,
            name=self.entry,
            persistent=True,
            allow_reentry=True,
        )  # this is a main handler for processing callbacks

    def send_page(self, update: Update, context: CallbackContext):
        '''reply - replies to user message and returns him page markup'''
        # get translated text
        text = self.get_string(f'text.{context.user_data.get(consts.TEXT)}')
        if context.user_data.get(consts.TEXT_VARS):
            # if you want to specify text variables then
            text = self.get_string(
                f'text.{context.user_data.get(consts.TEXT)}',
                **context.user_data.get(consts.TEXT_VARS)
            )

        markup = self.build_markup(update, context, 'en')

        with open(context.user_data.get(consts.PHOTO), 'rb') as photo:
            if context.user_data.get(consts.TG_PHOTO):
                photo = context.user_data.get(consts.TG_PHOTO)

            if update.callback_query:
                update.callback_query.edit_message_media(
                    media=InputMediaPhoto(photo),
                )  # send photo

                update.callback_query.edit_message_caption(
                    caption=text,
                    reply_markup=markup,
                )  # send text with keyboard markup

                update.callback_query.answer(
                    text='success',
                )  # pop up after succesful clicking on the button

            elif update.message:
                update.message.delete()  # remove user command

                if update.message.text == '/start':
                    # remove previous messages
                    self.delete_history(update, context)

                    with open(context.user_data.get(consts.PHOTO), 'rb') as photo:
                        message = update.message.reply_photo(
                            photo=photo,
                            caption=self.get_string(
                                f'text.{context.user_data.get(consts.TEXT)}'),
                            reply_markup=markup,
                        )
                        context.user_data[consts.HISTORY].append(
                            message)
                    # send photo with text and keyboard markup
                    # trying to load user data

                    try:
                        user_profile = User(
                            update.message.from_user.id)
                    except Exception:
                        self.create_user(update)
                else:
                    last = context.user_data.get(
                        consts.HISTORY)[-1]

                    update.message.bot.edit_message_media(
                        chat_id=last['chat_id'],
                        message_id=last['message_id'],
                        media=InputMediaPhoto(photo),
                    )  # send photo
                    update.message.bot.edit_message_caption(
                        chat_id=last['chat_id'],
                        message_id=last['message_id'],
                        caption=text,
                        reply_markup=markup,
                    )  # send text with keyboard markup

    def main_handler(self, update: Update, context: CallbackContext):

        context.user_data.update(
            {
                consts.TEXT: self.text,
                consts.PHOTO: self.photo,
                consts.KEYBOARD: self.keyboard
            }
        )

        self.custom_handler(update, context)
        self.add_back_button(update, context)  # builds back button
        self.send_page(update, context)  # reply to user sended message

        return self.entry  # return main state

    def add_back_button(self, update: Update, context: CallbackContext):
        '''
        back enters every time when user pressing button
        it draws back button
        '''

        history = context.user_data.get(consts.BACK)

        if not history:
            history = []

        if (len(history) > 1) and (history[-2] == self.entry):
            history.pop()
        else:
            history.append(self.entry)

        if len(history) > 1:
            context.user_data.update(
                {
                    consts.KEYBOARD_DYNAMIC: [
                        [
                            [
                                'back', history[-2]
                            ]
                        ]
                    ]
                }
            )

        context.user_data.update(
            {
                consts.BACK: history
            }
        )

    def build_markup(self, update: Update, context: CallbackContext, lang: str = 'en'):
        '''build_markup - builds a markup from keyboard and other buttons for sending it to user'''
        m = []

        if context.user_data.get(consts.KEYBOARD):
            m = [
                [
                    InlineKeyboardButton(text=self.get_string(f'buttons.{key[0]}', lang), callback_data=key[1]) for key in raw
                ] for raw in context.user_data.get(consts.KEYBOARD)
            ]

        if context.user_data.get(consts.KEYBOARD_DYNAMIC):
            m.extend(
                [
                    [
                        InlineKeyboardButton(text=self.get_string(f'buttons.{key[0]}', lang), callback_data=key[1]) for key in raw
                    ] for raw in context.user_data.get(consts.KEYBOARD_DYNAMIC)
                ]
            )

        # print(context.user_data.get(consts.KEYBOARD))
        # print(context.user_data.get(consts.KEYBOARD_DYNAMIC))
        # print()

        return InlineKeyboardMarkup(m)

    def get_string(self, text: str, lang: str = 'en', *args, **kwargs):
        '''
        get_string - takes text_id and language parameters and returnes you translation of it
        you need to specify text like so 'buttons.id'
        '''
        i18n.load_path.append('i18n')  # load translation dir
        # extract text by id and lang
        return i18n.t(f'{text}', locale=lang, *args, **kwargs)

    def delete_history(self, update: Update, context: CallbackContext):

        messages_history = context.user_data.get(consts.HISTORY)

        if not messages_history:
            messages_history = []

        if update.message:
            bot = update.message.bot
        else:
            bot = update.callback_query.bot

        for message in messages_history[::-1]:
            try:
                bot.delete_message(
                    chat_id=message['chat']['id'],
                    message_id=message['message_id']
                )
            except telegram.error.BadRequest:
                pass  # !!! we should handle errors

            messages_history.pop()

        context.user_data.update(
            {
                consts.HISTORY: messages_history
            }
        )

    def create_user(self, update: Update):
        user = update.message.from_user
        chat = update.message.bot.get_chat(chat_id=user.id).to_dict()
        photos = update.message.bot.getUserProfilePhotos(user_id=user.id)

        name = f'{user.first_name} ' if user.first_name else ""
        name += f'{user.last_name}' if user.last_name else ""

        user_profile = User()
        user_profile['id'] = str(user.id)
        user_profile['name'] = name
        user_profile['description'] = chat.get("bio")
        user_profile['tg-username'] = user.username
        user_profile['language'] = user.language_code
        user_profile['photo'] = photos["photos"][-1][0]['file_id'] if photos['total_count'] > 0 else None
        user_profile.save()
        user_profile.close()

    def custom_handler(self, update: Update, context: CallbackContext):
        pass
