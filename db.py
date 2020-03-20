import sqlite3
import sys


def create_db(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS drinks (name TEXT NOT NULL, in_stock INT NOT NULL);")
    print("Table drinks created successfully")
    drinks_name = conn.execute("SELECT name FROM drinks")
    if len(drinks_name.fetchall()) == 0:
        drinks = ['coca', 'ice tea', 'fuze tea', 'oasis tropical', 'oasis pcf', 'orangina', 'sprite', 'café', 'thé fruit rouge', 'thé menthe', 'thé noir',
                  'fanta', 'redbull', 'redbull bleue', 'redbull jaune', 'redbull orange', 'redbull blanche', 'monster', 'eau', 'volvic citron', 'tropico']
        for drink in drinks:
            conn.execute(
                f"INSERT INTO drinks (name,in_stock) VALUES ('{drink}', 1)")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS snacks (name TEXT NOT NULL, in_stock INT NOT NULL);")
    print("Table snacks created successfully")
    snacks_name = conn.execute("SELECT name FROM snacks")
    if len(snacks_name.fetchall()) == 0:
        snacks = ['lion peanuts', 'pitch', 'crunch', 'm&ms', 'maltesers', 'kit kat',
                  'kinder bueno', 'kinder bueno white', 'snickers', 'twix', 'skittles']
        for snack in snacks:
            conn.execute(
                f"INSERT INTO snacks (name,in_stock) VALUES ('{snack}', 1)")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS orders (items TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
    print("Table orders created successfully")
    conn.commit()
    return conn


def open_db():
    try:
        conn = sqlite3.connect('clickncollect.db', check_same_thread=False)
        conn.row_factory = lambda c, r: dict(
            [(col[0], r[idx]) for idx, col in enumerate(c.description)])
    except:
        print("error while loading database.")
        sys.exit(1)
    print('Opened database successfully')
    return create_db(conn)
