import peewee as pw
import difflib
from . import schema

# TODO: subclasses for each table in the database?
# TODO: Add methods to interact with the new metadata and episode tables



class ShowDB(object):
    def __init__(self, dbname):
        self.db = pw.SqliteDatabase(dbname)
    db = schema.db

    @property
    def all_shows(self):
        r = schema.Show.select(schema.Show.name)
        return([i.name for i in r])

    @property
    def all_aliases(self):
        r = schema.Alias.select(schema.Alias.alias_name)
        return([i.alias_name for i in r])

    def add_show(self, name, tvdb_id=None, tvdb_season=1):
        try:
            with self.db.transaction():
                l_name = name.strip().lower()
                new_show = schema.Show.create(name=l_name)

                new_alias = schema.Alias.create(
                    alias_name=l_name,
                    parent_show=new_show
                )

                new_meta = schema.Metadata.create(
                    name=l_name,
                    parent_show=new_show,
                    tvdb_id=tvdb_id,
                    tvdb_season=tvdb_season,
                )
        except Exception as e:
            print("Error adding show: {}".format(e))

    def delete_show(self, name):
        try:
            with self.db.transaction():
                l_name = name.strip().lower()

                schema.Show.get(
                    schema.Show.name == l_name
                ).delete_instance(recursive=True)
        except Exception as e:
            print("Error adding show: {}".format(e))

    def add_alias(self, alias_name, show_name):
        try:
            with self.db.transaction():
                l_alias_name = alias_name.strip().lower()
                l_target_name = show_name.strip().lower()

                parent_show = schema.Show.get(
                    schema.Show.name == l_target_name,
                )

                schema.Alias.create(
                    parent_show=parent_show,
                    alias_name=l_alias_name,
                )
        except Exception as e:
            print("Error adding show: {}".format(e))

    def lookup(self, name):
        try:
            l_name = name.strip().lower()

            r = (
                schema
                .Show
                .select()
                .join(schema.Alias)
                .where(schema.Alias.alias_name == l_name)
                .get()
            )

            return(r.name)
        except pw.DoesNotExist:
            return(None)

    def fuzzy_lookup(self, name):
        try:
            l_name = name.strip().lower()
            m = difflib.get_close_matches(l_name, self.all_aliases)

            r = set(
                (
                schema
                .Show
                .get(schema.Show.name == i)
                .name
                )
                for i in m
            )

            return(r)
        except pw.DoesNotExist:
            return(set())
