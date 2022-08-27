import sqlite3


def db():
    db = sqlite3.connect('poup.sqlite', check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db
