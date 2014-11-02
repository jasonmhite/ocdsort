from peewee import *
import datetime

db = SqliteDatabase("test.db", **{})

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

if __name__ == '__main__':
    db.create_tables([Show, Alias, Episode, Metadata])

#show = Show(name="Test Show")
#show.save()

#alias = Alias(alias_name="Test show alias", parent_show=show)
#alias.save()

#episode = Episode(parent_show=show, download_name="Test.mkv", parsed_episode=5)
#episode.save()

#meta = Metadata(parent_show=show, tvdb_id="193945")
#meta.save()
