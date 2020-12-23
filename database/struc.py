filename = "database/dataBase.db"

user_keys = ['id', 'name', 'description',
             'photo', 'rating', 'channel', "language", "location", 'tg-username']

deal_keys = ['id', 'user-id',
             'headline', 'description', 'pickup-location', 'delivery-locations',
             'price-list', 'photo', 'likes', 'dislikes', 'hashtags']

commit_keys = ['id', 'by', 'on', 'rating', 'text']

USERS = "user"
DEALS = "deal"
COMMITS = "comment"

nav = {USERS: user_keys, DEALS: deal_keys, COMMITS: commit_keys}


MIN = "min"
MAX = "max"
DEFAULT = "default"
REQUIRED = "required"
OPTIONS = "options"
TYPE = []


settings = {
    USERS: {
        "description": {
            MAX: 100,
        },


    }
}
