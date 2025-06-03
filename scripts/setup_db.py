import sqlite3
from lib.db.connection import DB_PATH

def setup():
    with open("lib/db/schema.sql") as f:
        schema = f.read()
    
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup()
