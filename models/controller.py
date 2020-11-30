
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Handler)

from models import consts, page


class Controller:
    # Controller is a page back-end, it handles all the clicks and messages
    # and builds everytime a new page

    controllers: list = []  # pages

    def __init__(self, controllers: list = []):
        self.controllers = controllers  # maybe delete
        self.page = page.Page(controllers)
        self.markup = self.page.markup()
        self.states = {
            # states needs to be like that = 'home'+'admin': [controller if controller.permission = 'admin']
            self.entry: [controller.build().conv()
                         for controller in controllers]
        }

    def handler(self, update: Update, context: CallbackContext):
        # handler is a default handler starts always when user pressed inline button that leads to another page

        self.push_back(update, context)  # add page to back button stack

        # reply to user action
        if update.callback_query:
            update.callback_query.edit_message_text(
                text=self.page.text,
                reply_markup=self.markup,
                parse_mode=telegram.ParseMode.HTML
            )
            update.callback_query.answer()
        elif update.message:
            if update.message.text:
                update.message.reply_text(
                    text=self.page.text,
                    reply_markup=self.markup,
                    parse_mode=telegram.ParseMode.HTML
                )

        return self.entry

    def conv(self):
        # conv is a default conversation handler describes all states and options like go to pages
        # so it builds the hole page and handles all the buttons in it in each state

        return ConversationHandler(
            entry_points=[
                CommandHandler(self.entry, self.handler) if self.entry == consts.HOME
                else CallbackQueryHandler(self.handler, pattern=f'^{self.entry}$'),

            ],
            states=self.states,
            fallbacks=[
                CallbackQueryHandler(
                    self.back_handler, pattern=f'^{self.entry}$'),
            ],
        )

    def back_handler(self, update: Update, context: CallbackContext):
        # back_handler is a handler that runs when back button is pressed
        # it works alongside with push_back function that handles the road of user in bot pages hierarchy

        if len(context.user_data.get(consts.BACK)) > 1 and update.callback_query.data == context.user_data.get(consts.BACK)[-2]:
            context.user_data[consts.BACK].pop()
            context.user_data[consts.BACK].pop()

        return self.handler(update, context)

    def push_back(self, update: Update, context: CallbackContext):
        # push_back makes it easy to look the road map of user in the bot to take him back when back button is pressed

        if not context.user_data.get(consts.BACK):
            context.user_data.update({consts.BACK: []})
            context.user_data[consts.BACK].append(f'{self.entry}')

        if update.callback_query:
            # if callback is equal to home page
            # clear back navigation list
            # or if not then add back button
            if update.callback_query.data == consts.HOME:
                context.user_data.update({consts.BACK: []})
            else:
                back = [
                    InlineKeyboardButton(
                        text=consts.BACK, callback_data=f'{context.user_data.get(consts.BACK)[-1]}')
                ]
                self.page.back_func([back])
                self.markup = self.page.markup()

            context.user_data[consts.BACK].append(f'{self.entry}')

    def handle_func(self, handler, text: str = '', pattern: str = ''):
        # handle_func is a handler for buttons that doesn't deal with pages
        # you can use it to proccess some algorithms by clicking button
        if isinstance(handler, Controller):
            self.states[self.entry].append(
                handler.build().conv()
            )  # add handler to our state
            self.markup = self.page.markup([
                [InlineKeyboardButton(text=text, callback_data=handler.entry)]
            ])  # add button to our page
        elif isinstance(handler, Handler):
            self.states[self.entry].append(
                handler,
            )
        else:
            self.states[self.entry].append(
                CallbackQueryHandler(handler, pattern=f'^{pattern}$')
            )  # add handler to our state
            self.markup = self.page.markup([
                [InlineKeyboardButton(text=text, callback_data=pattern)]
            ])  # add button to our page

    # deprecated

    # def back(self, update: Update, context: CallbackContext):
    #     # another option to handle back button by storing one parent page in each page (depricated)

    #     if not context.user_data.get(self.entry):
    #         print('context(consts.BACK)', context.user_data.get(consts.BACK))
    #         print('context(self.entry)', context.user_data.get(self.entry))
    #         print('self.entry', self.entry)
    #         print()
    #         context.user_data.update({
    #             self.entry: context.user_data.get(consts.BACK)
    #         })
    #         context.user_data.update({
    #             consts.BACK: self.entry
    #         })

    #     if self.entry != consts.HOME:
    #         self.markup = self.page.markup([
    #             [InlineKeyboardButton(
    #                 text=consts.BACK, callback_data=f'{context.user_data.get(self.entry)}')]
    #         ])

    # def goto(self, controller):
    #         # add controller to states and
    #         # -----
    #         # image
    #         # text
    #         # button
    #         # -----
    #         # controller.build()

    #         def handler1(self, update: Update, context: CallbackContext):
    #             self.handler(update, context)

    #         self.handle_func(controller.entry, controller.entry, handler1)

    #         self.controllers.append()
    #         # self.markup = self.page.markup()
    #         # goto needs to build controller and send it when needs
