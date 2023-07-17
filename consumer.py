import pika
from mongoengine import connect, Document, StringField, BooleanField


# Підключення до бази даних MongoDB
connect(
    host=f"""mongodb+srv://NickoSuerte:Nick1987Burjuy@cluster0.tquscaz.mongodb.net/hw8?retryWrites=true&w=majority""", ssl=True)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)


# Функція для обробки повідомлення та імітації відправлення email
def process_message(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending email to {contact.email}...")
        contact.sent = True
        contact.save()
        ch.basic_ack(delivery_tag=method.delivery_tag)


# Скрипт для споживання повідомлень з черги
def main():
    # Підключення до RabbitMQ та створення черги
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    # Вказуємо, що можна отримувати одне повідомлення одночасно
    channel.basic_qos(prefetch_count=1)

    # Встановлюємо функцію для обробки повідомлень
    channel.basic_consume(queue='email_queue',
                          on_message_callback=process_message)

    print("Consumer started. Waiting for messages...")
    channel.start_consuming()


if __name__ == '__main__':
    main()
