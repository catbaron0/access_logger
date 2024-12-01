import os
from pathlib import Path

from peewee import SqliteDatabase, Model, CharField, DateTimeField


DB_PATH = os.environ.get('ACCESS_DB_PATH')
if not DB_PATH:
    DB_PATH = "."

database = SqliteDatabase(Path(DB_PATH) / 'access.db')

class Access(Model):
    datetime = DateTimeField()
    ip = CharField()
    agent = CharField()
    country = CharField(null=True)
    city = CharField(null=True)
    provider = CharField(null=True)
    host = CharField()
    uri = CharField()
    referer = CharField()


    class Meta:
        database = database
