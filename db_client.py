from tinydb import TinyDB, Query

db = TinyDB('database/db.json')
users_table = db.table(name='Users')
urls_table = db.table(name='URLs')

def create_new_url():
    pass

def create_new_user(user_id):
    User = Query()
    query_response = users_table.search(User.user_id == user_id)

    if len(query_response) > 0:
        return False

    else:
        users_table.insert(
            {
                'user_id' : user_id,
                'hits' : 0,
                'url_count' : 0
            }
        )
        return True
