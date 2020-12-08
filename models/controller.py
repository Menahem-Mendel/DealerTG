
import i18n
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Dispatcher,
                          Filters, Handler, MessageHandler)

from models import consts


class Page:
    photo = 'assets/img/home.png'
    entry = 'base'
    text = 'base'

    def __init__(self, states: dict = {}, keyboard: list = []):
        # keyboard is a [[[text_id, callback]]] which is converted to buttons
        self.keyboard = keyboard

        self.handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.handler_func) if self.entry == consts.HOME
                else CallbackQueryHandler(self.handler_func, pattern=rf"^{self.entry}$"),
            ],  # entry_points sepcifies the entry handlers
            states=states,  # states is a conversation branches, for example if user pressed button it activates the returned state, and only few of callbacks can be processed
            fallbacks=[
                CallbackQueryHandler(
                    self.back_handler, pattern=rf"^{self.entry+consts.BACK}$"),
                CallbackQueryHandler(
                    self.handler_func, pattern=rf"^{consts.DONE}$")  # when branch work is done return to main
            ],  # if you want to back to main state then specify this handlers
            # map_to_parent={
            #     consts.END: self.entry,
            # },  # if you had returened to main handler but you want to map your previous state to some other state then specify it here [main state: current state]
            name=self.entry,
            persistent=True,
        )  # this is a main handler for processing callbacks

    def build(self, lang: str = 'en', btns: list = []):
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

    def get_string(self, text: str, lang: str = 'en'):
        '''
        get_string - takes text_id and language parameters and returnes you translation of it
        you need to specify text like so 'buttons.id'
        '''
        i18n.load_path.append('i18n')  # load translation dir
        return i18n.t(f'{text}', locale=lang)  # extract text by id and lang

    def reply(self, update: Update, context: CallbackContext):
        '''reply - replies to user message and returns him page markup'''
        if update.callback_query:
            with open(self.photo, 'rb') as photo:
                update.callback_query.edit_message_media(
                    media=InputMediaPhoto(photo),
                )  # send photo

                update.callback_query.edit_message_caption(
                    caption=self.get_string(
                        f'text.{self.text}', context.user_data.get('lang')),
                    reply_markup=InlineKeyboardMarkup(self.markup),
                    parse_mode=ParseMode.HTML,
                )  # send text with keyboard markup

            '''alternative'''
            # update.callback_query.message.delete()
            # with open(self.photo, 'rb') as photo:
            #     update.callback_query.message.reply_photo(
            #         photo=photo,
            #         caption=f'{self.text}',
            #         reply_markup=InlineKeyboardMarkup(self.markup),
            #         parse_mode=ParseMode.HTML,
            #     )  # send photo with text

            update.callback_query.answer(
                text='fuck',
            )  # pop up after succesful clicking on the button
        elif update.message:
            with open(self.photo, 'rb') as photo:
                update.message.delete()  # remove user command
                update.message.reply_photo(
                    photo=photo,
                    caption=self.get_string(
                        f'text.{self.text}', context.user_data.get('lang')),
                    reply_markup=InlineKeyboardMarkup(self.markup),
                    parse_mode=ParseMode.HTML,
                )  # send photo with text and keyboard markup

    def handler_func(self, update: Update, context: CallbackContext):
        context.user_data['lang'] = 'en'  # specify language

        # build keyboard markup with proper localization
        self.markup = self.build(lang=context.user_data.get('lang'))

        self.back(update, context)  # builds back button
        self.reply(update, context)  # reply to user sended message

    '''
    option 1:
    
    make history for back button like so context.user_data['back'] == ['home', 'deals', 'profile']
    and when clicking back button - back_handler removes two last entries, for examples if i pressed 'back'
    then context.user_data['back'] == ['home'] but because i'm adding current page then it'll look like so
    then context.user_data['back'] == ['home', 'deals']

    pros: simplisity
    cons: not proffesional

    option 2:
    
    remember back button for each page like so context.user_data['deals'] = 'home' and if user pressed back
    then we say that context.user_data['back'] == 'deals' to remember for next page from where we came up.
    now if we'll move to 'profile', then we say that context.user_data['profile'] = context.user_data['back'] == 'deals'
    and context.user_data['back'] = 'profile'

    pressed 'deals'
    {
        entry is 'deals'
        context['back'] is 'home'
        context['deals'] = context['back']
        context['back'] = entry
    }
    pressed 'profile'
    {
        entry is 'profile'
        context['back'] is 'deals'
        context['deals'] = context['back']
        context['back'] = entry
    }
    when the back button is pressed then back_handler is activated and it changing the context['back']
    pressed 'back'
    {
        back_handler:
            entry is 'deals'
            context['back'] = context[entry] # 'home'
        back:
            entry is 'deals'
            context['back'] is 'home'
            context['deals'] = context['back']
            context['back'] = entry
    }
    pros: prof
    cons: cicle pages
    '''

    # !!!
    def back(self, update: Update, context: CallbackContext):
        '''
        back enters every time when user pressing button
        it draws back button
        '''

        if context.user_data.get(consts.BACK) != self.entry+consts.BACK and context.user_data.get(context.user_data.get(self.entry+consts.BACK)) and context.user_data.get(self.entry+consts.BACK) != context.user_data.get(context.user_data.get(self.entry+consts.BACK)):
            context.user_data[self.entry +
                              consts.BACK] = context.user_data.get(consts.BACK)
            context.user_data[consts.BACK] = self.entry+consts.BACK

        print(
            f'entry = {self.entry}\n'
            f'context[self.entry] = {context.user_data.get(self.entry+consts.BACK)}\n'
            f'context[consts.BACK] = {context.user_data.get(consts.BACK)}\n'
        )

        if context.user_data.get(self.entry+consts.BACK) and self.entry != consts.HOME:
            self.markup = self.build(
                lang=context.user_data.get('lang'),
                btns=[
                    [
                        [
                            'back',
                            context.user_data.get(self.entry+consts.BACK)
                        ],
                    ],
                ])

    # !!!
    def back_handler(self, update: Update, context: CallbackContext):
        '''back_handler activates when back button is pressed'''
        print('was here')  # enters not when expected
        context.user_data[consts.BACK] = context.user_data.get(
            self.entry+consts.BACK)
        return self.handler_func(update, context)
