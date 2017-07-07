import sqlite3
import short_url

from sqlite3 import IntegrityError


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
        shortUrl TEXT NOT NULL,
        userId TEXT NOT NULL,
        FOREIGN KEY(userId) REFERENCES User(id) ON DELETE CASCADE
    )
""")

conn.commit()
conn.close()

def get_url(url_id):
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url FROM URL WHERE id = ?
    """, (url_id, ))

    data = cursor.fetchone()

    cursor.execute("""UPDATE URL SET hits=hits+1 WHERE id=?
    """, (url_id, ))

    conn.commit()
    conn.close()

    if data is None:
        return False, None

    else:
        return True, data[0]

def get_top_urls(user_id=None):
    conn = sqlite3.connect('database/challenge.db')
    cursor = conn.cursor()
    if user_id is None:
        cursor.execute("""
        SELECT * FROM URL ORDER BY hits DESC LIMIT 10
        """)
    else:
        cursor.execute("""
        SELECT * FROM URL WHERE userId=? ORDER BY hits DESC LIMIT 10
        """, (user_id, ))

    data = cursor.fetchall()
    conn.close()

    url_list = []
    for row in data:
        stats = {
            'id': row[0],
            'hits': row[1],
            'url': row[2],
            'shortUrl': row[3]
        }
        url_list.append(stats)

    return url_list

def get_user_stats(user_id): #TODO: test if top urls by user are right
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM User WHERE id = ?
    """, (user_id,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return False, None

    else:
        stats = {
            'id': data[0],
            'hits': data[1],
            'urlCount': data[2]
            'topUrls': get_top_urls(user_id)
        }
        return True, stats

def get_url_stats(url_id):
    conn = sqlite3.connect('database/challenge.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM URL WHERE id = ?
    """, (url_id, ))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return False, None

    else:
        stats = {
            'id': data[0],
            'hits': data[1],
            'url': data[2],
            'shortUrl': data[3]
        }
        return True, stats

def get_global_stats():
    conn = sqlite3.connect('database/challenge.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(), sum(hits) FROM URL
    """)
    data = cursor.fetchone()
    conn.commit()
    conn.close()

    url_count = data[0]
    hits_sum = data[1]
    top_urls = get_top_urls()

    response = {
        'hits': hits_sum,
        'urlCount': url_count,
        'topUrls': top_urls
    }

    return response

def create_new_url(url, partial_short_url, user_id): #TODO: incremment user url count
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO URL (hits, url, shortUrl, userId) VALUES (?, ?, ?, ?)
        """, (0, url, partial_short_url, user_id))

        url_id = cursor.lastrowid
        shortened_url = str(partial_short_url + '/' + str(short_url.encode_url(url_id)))

        cursor.execute("""
            UPDATE URL SET shortUrl=? WHERE id=?
            """, (shortened_url, url_id))

        conn.commit()
        conn.close()
        resp, stats = get_url_stats(url_id) #Will always return the correct URL

        return True, stats

    except IntegrityError as err:
        print('Error. Insert URL failed due to violation of FK constraints.')
        conn.rollback()
        conn.close()

        return False, None

def create_new_user(user_id):
    conn = sqlite3.connect('database/challenge.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO User (id, hits, urlCount) VALUES (?, ?, ?)
        """, (user_id, 0, 0))
        conn.commit()
        conn.close()
        return True

    except IntegrityError as err:
        print('Error. User already registered.')
        conn.rollback()
        conn.close()
        return False

def delete_user(user_id):
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM User WHERE id=?
    """, (user_id, ))
    conn.commit()
    conn.close()

def delete_url(url_id): #TODO: decrement user url count
    conn = sqlite3.connect('database/challenge.db')
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM URLs WHERE id=?
    """, (url_id, ))
    conn.commit()
    conn.close()
