from mongoengine import Document, StringField, DateTimeField, ReferenceField
from mongoengine import BooleanField, ListField
from mongoengine import connect
connect(
    host=f"""mongodb+srv://NickoSuerte:Nick1987Burjuy@cluster0.tquscaz.mongodb.net/hw8?retryWrites=true&w=majority""", ssl=True)


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author)
    quote = StringField()


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
