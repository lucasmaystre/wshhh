import datetime
import os.path

from flask_login import UserMixin
from peewee import (Model, PrimaryKeyField, TextField, IntegerField,
                    DateTimeField, ForeignKeyField, SqliteDatabase)


DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'data', 'database.db'))
DATABASE = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = DATABASE


class User(BaseModel, UserMixin):
    id = PrimaryKeyField()
    email = TextField(index=True)
    pw_hash = TextField()


class Item(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, related_name="items", index=True)
    created = DateTimeField(default=datetime.datetime.now)


class Attribute(BaseModel):
    id = PrimaryKeyField()
    filename = TextField()
    description = TextField()


class ItemAttribute(BaseModel):
    id = PrimaryKeyField()
    item = ForeignKeyField(Item, index=True)
    attribute = ForeignKeyField(Attribute, index=True)


class Image(BaseModel):
    id = PrimaryKeyField()
    item = ForeignKeyField(Item, related_name="images", index=True)
    thumbnail_filename = TextField()
    fullres_filename = TextField()
