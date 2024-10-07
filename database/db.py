import sqlite3


class Database:

    def __init__(self, name):

        self.db_name = name
        self.conn = sqlite3.connect(name)
        self.cur = self.conn.cursor()

        self._create_tables()
        self.conn.close()

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def __del__(self):
        self.conn.close()

    def _create_tables(self):

        request = """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            status TEXT NOT NULL CHECK (status IN ('USER', 'ADMIN'))
        );
        CREATE TABLE IF NOT EXISTS giveaway (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL REFERENCES users(id),
            name TEXT NOT NULL,
            text TEXT,
            winners_count INTEGER NOT NULL DEFAULT 1,
            message_for_winner TEXT NOT NULL,
            message_for_others TEXT NOT NULL,
            end_datetime DATETIME,
            status TEXT NOT NULL CHECK (status IN ('CREATING', 'PENDING', 'RUN', 'FINISHED')) DEFAULT 'CREATING'
        );
        CREATE TABLE IF NOT EXISTS giveaway_participants (
            user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            giveaway_id TEXT NOT NULL REFERENCES giveaway(id) ON DELETE CASCADE,
            is_winner INTEGER CHECK (is_winner in (0, 1)) DEFAULT 0,
            UNIQUE (user_id, giveaway_id)
        );
        PRAGMA foreign_keys = ON;
        """

        self.cur.executescript(request)
        self.conn.commit()

    def _drop_table(self, table_name):
        self.cur.execute(f"DROP TABLE {table_name};")
        self.conn.commit()

    def insert(self, request_template: str, params: tuple = None):

        if params:
            self.cur.execute(request_template, params)
        else:
            self.cur.execute(request_template)
        self.conn.commit()

    def update(self, request_template: str, params: tuple = None):

        if params:
            self.cur.execute(request_template, params)
        else:
            self.cur.execute(request_template)
        self.conn.commit()

    def delete(self, request_template: str, params: tuple = None):

        if params:
            self.cur.execute(request_template, params)
        else:
            self.cur.execute(request_template)
        self.conn.commit()

    def select(self, request_template: str, params: tuple = None):
        if params:
            self.cur.execute(request_template, params)
        else:
            self.cur.execute(request_template)
        return self.cur.fetchall()


if __name__ == "__main__":
    db = Database("db.sqlite3")

