from models import Author, Quote

while True:
    user_input = input("Введіть команду: ")

    if user_input == 'exit':
        break

    command, value = user_input.split(':')
    command = command.strip()
    value = value.strip()

    if command == 'name':
        author = Author.objects(fullname=value).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print("Автор не знайдений")

    elif command == 'tag':
        quotes = Quote.objects(tags=value)
        for quote in quotes:
            print(quote.quote)

    elif command == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(quote.quote)

    else:
        print("Невідома команда")
