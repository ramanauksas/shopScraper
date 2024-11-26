import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",  # localhost
        user='root',
        password='root',
        database="supermarkets",
        port="3309",
    )
    return conn

class DB:
    def __init__(self):
        self.conn = connect_db()

    def close(self):
        self.conn.close()