from peewee import AutoField, CharField, Model, SqliteDatabase, TextField


database = SqliteDatabase("hiraizoomin.db")


class Place(Model):
    id = AutoField()
    name_en = CharField()
    name_ja = CharField(null=True)
    category = CharField()
    description = TextField()
    placeholder_key = CharField()
    address = TextField(null=True)
    google_maps_url = TextField()
    opening_hours = CharField(null=True)

    class Meta:
        database = database
