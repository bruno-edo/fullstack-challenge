import sqlite3
import short_url

from sqlite3 import IntegrityError

#TODO: change these commands to a setup file, that will be executed as part of the setup process
conn = sqlite3.connect('database/challenge.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        id TEXT NOT NULL PRIMARY KEY
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

#TODO: maybe change the boolean returns to exceptions being raised
def get_url(url_id):
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url FROM URL WHERE id = ?
    """, (url_id, ))

    data = cursor.fetchone()

    if data is None:
        conn.close()
        return False, None

    else:
        cursor.execute("""UPDATE URL SET hits=hits+1 WHERE id=?
        """, (url_id, ))

        conn.commit()
        conn.close()

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

def get_user_stats(user_id):
    conn = sqlite3.connect('database/challenge.db')
    conn.execute('pragma foreign_keys=ON') #Turns on foreign key constraints
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM User WHERE id = ?
    """, (user_id,))
    data = cursor.fetchone()


    if data is None:
        conn.close()
        return False, None

    else:
        urls = get_top_urls(user_id)
        hits = 0
        for url in urls:
            hits += int(url['hits'])

        stats = {
            'id': data[0],
            'hits': hits,
            'topUrls': urls
        }

        cursor.execute("""
            SELECT count() FROM URL WHERE userId = ?
        """, (user_id, ))
        data = cursor.fetchone()
        url_count = data[0]
        conn.close()

        stats['urlCount'] = url_count

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
        conn.close()
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

def create_new_url(url, partial_short_url, user_id):
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
            INSERT INTO User (id) VALUES (?)
        """, (user_id, ))
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

def delete_url(url_id):
    conn = sqlite3.connect('database/challenge.db')
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM URL WHERE id=?
    """, (url_id, ))

    conn.commit()
    conn.close()
