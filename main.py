
import html
import json
import logging
import traceback

from telegram import ParseMode, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, PicklePersistence, Updater, CallbackQueryHandler)

import config
import pages.deals
#     # Finally, send the message
#     update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
import pages.home
import pages.profile
import pages.search
from models import consts
from utils.logger import *

DEVELOPER_CHAT_ID = 689568164


def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb)}</pre>'
    )

    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID,
                             text=message, parse_mode=ParseMode.HTML)


def back(update: Update, context: CallbackContext):
    handler = context.user_data.get(consts.BACK)[-2]

    context.user_data[consts.BACK].pop()
    context.user_data[consts.BACK].pop()

    return handler.handler_func(update, context)


def main():
    updater = Updater(config.token)
    dp = updater.dispatcher

    dp.add_handler(pages.home.Home)
    dp.add_handler(pages.search.Search)
    dp.add_handler(pages.deals.Deals)
    dp.add_handler(pages.profile.Profile)

    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
