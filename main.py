
import html
import json
import logging
import traceback

from telegram import ParseMode, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, PicklePersistence, Updater, CallbackQueryHandler)

import config
import pages.deals
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

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
    )

    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID,
                             text=message, parse_mode=ParseMode.HTML)


def main():
    pp = PicklePersistence(filename='pickle.pickle')
    updater = Updater(config.token, persistence=pp)
    # updater = Updater(config.token)
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
