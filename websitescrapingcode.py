import requests
from bs4 import BeautifulSoup
import json

# Отримання HTML-сторінки
response = requests.get('http://quotes.toscrape.com')
html = response.text

# Парсинг HTML-сторінки з використанням BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Отримання цитат та авторів
quotes = []
authors = []

quote_elements = soup.select('.quote')
for quote_element in quote_elements:
    text = quote_element.select_one('.text').text
    author = quote_element.select_one('.author').text
    tags = [tag.text for tag in quote_element.select('.tag')]

    quotes.append({'text': text, 'author': author, 'tags': tags})
    authors.append(author)

# Запис цитат у файл quotes.json
with open('quotes.json', 'w') as file:
    json.dump(quotes, file, indent=4)

# Запис авторів у файл authors.json
unique_authors = list(set(authors))
authors_data = [{'fullname': author} for author in unique_authors]

with open('authors.json', 'w') as file:
    json.dump(authors_data, file, indent=4)

print("Скрапінг завершено. Дані збережені у файлах quotes.json та authors.json.")
