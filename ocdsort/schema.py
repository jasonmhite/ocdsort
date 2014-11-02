from peewee import *
import datetime
from . import config

db = SqliteDatabase(config.config["paths"]["db"], **{})

class BaseModel(Model):
    class Meta:
        database = db

class Show(BaseModel):
    name = CharField(unique=True)

class Alias(BaseModel):
    alias_name = TextField(null=True, unique=True)
    parent_show = ForeignKeyField(
        Show,
        related_name="aliases",
        on_delete="CASCADE",
    )

class Episode(BaseModel):
    parent_show = ForeignKeyField(
        Show,
        related_name="episodes",
        on_delete="CASCADE",
    )
    download_name = TextField(null=True)
    download_time = DateTimeField(
        default=datetime.datetime.now,
        null=False,
    )
    parsed_episode = IntegerField(null=True)

class Metadata(BaseModel):
    parent_show = ForeignKeyField(
        Show,
        related_name="metadata",
        on_delete="CASCADE",
        unique=True,
    )
    tvdb_id = TextField(null=True, unique=True)
    tvdb_season = IntegerField(null=False, default=1)

def init_db(filename):
    db.create_tables([Show, Alias, Episode, Metadata])
