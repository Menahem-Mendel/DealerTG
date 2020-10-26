from telegram.ext.conversationhandler import ConversationHandler

(
    MENU,
    HOME_MENU,
    SEARCH_MENU,
    DEALS_MENU,
    ADDING_DEAL

) = map(chr, range(5))

END = ConversationHandler.END

HOME = 'home'
SEARCH = 'search'
DEALS = 'deals'
LOCATION = 'location'
BACK = 'back'
BLA = 'bla'
