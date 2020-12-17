filename = "../../dealerBotMendel/DealerTG/database/dataBase.db"

user_keys = ['id', 'name', 'description', 'photo', 'raiting', 'channel', 'tg-username']

deal_keys = ['id', 'user-id',
             'headline', 'description', 'pickup-location', 'delivery-locations',
             'price-list', 'photo', 'likes', 'dislikes', 'hashtags']

commit_keys = ['id', 'by', 'on', 'raiting', 'text']

USERS = "user"
DEALS = "deal"
COMMITS = "comment"

nav = {USERS: user_keys, DEALS: deal_keys, COMMITS: commit_keys}

