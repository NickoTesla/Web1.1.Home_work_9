import json
from models import Author, Quote
from models import connect

# Завантаження авторів
with open('data.json/authors.json', 'r', encoding="utf8") as file:
    authors_data = json.load(file)
    for author_data in authors_data:
        author = Author(**author_data)
        author.save()

# Завантаження цитат
with open('data.json/quotes.json', 'r', encoding="utf8") as file:
    quotes_data = json.load(file)
    for quote_data in quotes_data:
        author_fullname = quote_data.pop('author')
        author = Author.objects(fullname=author_fullname).first()
        quote_data['author'] = author
        quote = Quote(**quote_data)
        quote.save()
