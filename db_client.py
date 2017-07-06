import sqlite3

conn = sqlite3.connect('database/challenge.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        id TEXT NOT NULL PRIMARY KEY,
        hits INTEGER NOT NULL,
        urlCount INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS URL (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        hits INTEGER NOT NULL,
        url TEXT NOT NULL,
        sortUrl TEXT NOT NULL,
        userId TEXT NOT NULL,
        FOREIGN KEY(userId) REFERENCES User(id) ON DELETE CASCADE
    )
""")

def create_new_url():
    pass

def create_new_user(user_id):
    pass
    #User = Query()
    #query_response = users_table.search(User.user_id == user_id)

    #if len(query_response) > 0:
    #    return False

    #else:
    #    users_table.insert(
    #        {
    #            'user_id' : user_id,
    #            'hits' : 0,
    #            'url_count' : 0
    #        }
    #    )
    #    return True
