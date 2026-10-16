from peewee import AutoField, CharField, ForeignKeyField, IntegerField, Model, SqliteDatabase, TextField


database = SqliteDatabase("hiraizoomin.db")


class Place(Model):
    id = AutoField()
    name_en = CharField()
    name_ja = CharField(null=True)
    category = CharField()
    description = TextField()
    placeholder_key = CharField()
    image_filename = CharField(null=True)
    address = TextField(null=True)
    google_maps_url = TextField()
    opening_hours = CharField(null=True)

    class Meta:
        database = database


class PlacePhoto(Model):
    id = AutoField()
    place = ForeignKeyField(Place, backref="photos", on_delete="CASCADE")
    filename = CharField()
    sort_order = IntegerField()

    class Meta:
        database = database
        indexes = ((('place', 'sort_order'), False),)


def initialize_database():
    database.connect(reuse_if_open=True)
    database.create_tables([Place, PlacePhoto], safe=True)
    column_names = {column.name for column in database.get_columns("place")}
    if "image_filename" not in column_names:
        database.execute_sql('ALTER TABLE "place" ADD COLUMN "image_filename" VARCHAR(255)')

    for place in Place.select().where(Place.image_filename.is_null(False)):
        if place.image_filename and not PlacePhoto.select().where(
            (PlacePhoto.place == place) & (PlacePhoto.filename == place.image_filename)
        ).exists():
            PlacePhoto.create(place=place, filename=place.image_filename, sort_order=0)
    database.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialization complete.")
