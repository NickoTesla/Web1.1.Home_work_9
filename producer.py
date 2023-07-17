import json
import random
import string
import pika
from mongoengine import connect, Document, StringField, BooleanField


# Підключення до бази даних MongoDB
connect(
    host=f"""mongodb+srv://NickoSuerte:Nick1987Burjuy@cluster0.tquscaz.mongodb.net/hw8?retryWrites=true&w=majority""", ssl=True)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)


# Генерація випадкового email
def generate_email():
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com']
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for _ in range(8))
    domain = random.choice(domains)
    return f"{username}@{domain}"


# Генерація фейкових контактів та запис у базу даних
def generate_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        email = generate_email()
        contact = Contact(fullname='John Doe', email=email)
        contact.save()
        contacts.append(contact)
    return contacts


# Відправлення повідомлення по email (заглушка)
def send_email(contact):
    print(f"Sending email to {contact.email}...")
    contact.sent = True
    contact.save()


# Отримання повідомлення з черги та обробка
def process_message(ch, method, properties, body):
    contact_id = json.loads(body)
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_email(contact)
        ch.basic_ack(delivery_tag=method.delivery_tag)


# Скрипт для відправлення повідомлень у чергу
def main():
    num_contacts = 5
    contacts = generate_contacts(num_contacts)

    # Підключення до RabbitMQ та створення черги
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    # Відправлення повідомлень у чергу
    for contact in contacts:
        channel.basic_publish(
            exchange='', routing_key='email_queue', body=str(contact.id))

    connection.close()


if __name__ == '__main__':
    main()
