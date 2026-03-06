from peewee import SqliteDatabase

db = SqliteDatabase("app.db", pragmas={"journal_mode": "wal", "foreign_keys": 1})
