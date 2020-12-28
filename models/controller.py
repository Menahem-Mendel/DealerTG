
import i18n
import telegram
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update, Chat)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, Handler, MessageHandler)

from models import consts
from database.DataBase import User


class Page:
    photo = 'assets/img/home.png'
    tg_photo = None
    entry = 'base'
    text = 'base'

    def __init__(self, states: dict = {}, keyboard: list = []):
        # keyboard is a [[[text_id, callback]]] which is converted to buttons
        self.keyboard = keyboard

        self.handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.main_handler) if self.entry == consts.HOME
                else CallbackQueryHandler(self.main_handler, pattern=rf"^{self.entry}$"),
            ],  # entry_points sepcifies the entry handlers
            states=states,  # states is a conversation branches, for example if user pressed button it activates the returned state, and only few of callbacks can be processed
            fallbacks=[
                CallbackQueryHandler(
                    self.main_handler, pattern=rf"^{self.entry}$"),
            ],  # if you want to back to main state then specify this handlers
            name=self.entry,
            persistent=True,
            allow_reentry=True,
        )  # this is a main handler for processing callbacks

    def send_page(self, update: Update, context: CallbackContext):
        '''reply - replies to user message and returns him page markup'''
        if update.callback_query:

            if self.tg_photo is not None:
                photo = self.tg_photo
            else:
                photo = open(self.photo, 'rb')

            update.callback_query.edit_message_media(
                media=InputMediaPhoto(photo),
            )  # send photo

            update.callback_query.edit_message_caption(
                caption=self.text,
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )  # send text with keyboard markup

            update.callback_query.answer(
                text='fuck',
            )  # pop up after succesful clicking on the button
        elif update.message:
            with open(self.photo, 'rb') as photo:
                update.message.delete()  # remove user command
                if update.message.text and update.message.text.lower() == "/start":
                    self.start_handler(update, context)
                else:
                    last_message = context.user_data.get(
                        "messages_history")[-1]
                    update.message.bot.edit_message_media(
                        chat_id=last_message['chat_id'],
                        message_id=last_message['message_id'],
                        media=InputMediaPhoto(photo),
                    )  # send photo

                    update.message.bot.edit_message_caption(
                        chat_id=last_message['chat_id'],
                        message_id=last_message['message_id'],
                        caption=self.text,
                        reply_markup=InlineKeyboardMarkup(self.markup),
                        parse_mode=ParseMode.HTML,
                    )  # send text with keyboard markup

    def main_handler(self, update: Update, context: CallbackContext):
        # build keyboard markup with proper localization
        self.markup = self.build_keyboard()
        self.text = self.get_string(f'text.{self.text}')
        print(self.text, "texttt")

        self.custom_handler(update, context)

        self.add_back_button(update, context)  # builds back button
        self.send_page(update, context)  # reply to user sended message

        return self.entry  # return main state

    def start_handler(self, update: Update, context: CallbackContext):
        context.user_data['lang'] = 'en'
        self.delete_history(update, context)  # remove previous messages
        with open(self.photo, 'rb') as photo:
            message = update.message.reply_photo(
                photo=photo,
                caption=self.text,
                reply_markup=InlineKeyboardMarkup(self.markup),
                parse_mode=ParseMode.HTML,
            )
            context.user_data['messages_history'].append(message)
        # send photo with text and keyboard markup
        # trying to load user data
        try:
            user_profile = User(update.message.from_user.id)

        except Exception:
            self.create_user(update)

    def add_back_button(self, update: Update, context: CallbackContext):
        '''
        back enters every time when user pressing button
        it draws back button
        '''
        print("context", context.user_data.get('check'))
        context.user_data['check'] = True
        history = context.user_data.get('history')
        if history == None:
            history = []
        print('back history..', history)

        if len(history) > 1 and history[-2] == self.entry:
            history.pop()
        else:
            history.append(self.entry)
        print('back history 2..', history)

        if len(history) > 1:
            self.markup = self.build_keyboard(
                lang=context.user_data.get('lang'),
                btns=[
                    [
                        ['back', history[-2]],
                    ],
                ])
        context.user_data['history'] = history

    def build_keyboard(self, lang: str = 'en', btns: list = []):
        '''build - builds a markup from keyboard and other buttons for sending it to user'''

        m = [
            [
                InlineKeyboardButton(text=self.get_string(f'buttons.{key[0]}', lang), callback_data=key[1]) for key in raw
            ] for raw in self.keyboard
        ]  # making new array of keyboard buttons
        m.extend([
            [
                InlineKeyboardButton(text=self.get_string(f'buttons.{key[0]}', lang), callback_data=key[1]) for key in raw
            ] for raw in btns
        ])  # adding buttons

        return m

    def get_string(self, text: str, lang: str = 'en', *args, **kwargs):
        '''
        get_string - takes text_id and language parameters and returnes you translation of it
        you need to specify text like so 'buttons.id'
        '''
        i18n.load_path.append('i18n')  # load translation dir
        # extract text by id and lang
        return i18n.t(f'{text}', locale=lang, *args, **kwargs)

    def delete_history(self, update: Update, context: CallbackContext):
        messages_history = context.user_data.get("messages_history")
        if messages_history == None:
            messages_history = []

        if update.message == None:
            bot = update.callback_query.bot
        else:
            bot = update.message.bot

        for message in messages_history[::-1]:
            try:
                bot.delete_message(
                    chat_id=message['chat']['id'], message_id=message['message_id'])
            except telegram.error.BadRequest:
                pass
            messages_history.pop()
        context.user_data['messages_history'] = messages_history

    def custom_handler(self, update: Update, context: CallbackContext):
        pass

    def create_user(self, update: Update):
        user = update.message.from_user
        chat = update.message.bot.get_chat(chat_id=user.id).to_dict()
        photos = update.message.bot.getUserProfilePhotos(user_id=user.id)

        name = user.first_name + " " if user.first_name else ""
        name += user.last_name if user.last_name else ""

        user_profile = User()
        user_profile['id'] = str(user.id)
        user_profile['name'] = name
        user_profile['description'] = chat.get("bio")
        user_profile['tg-username'] = user.username
        user_profile['language'] = user.language_code
        user_profile['photo'] = photos["photos"][-1][0]['file_id'] if photos['total_count'] > 0 else None
        user_profile.save()
        user_profile.close()
