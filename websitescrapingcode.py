import requests
from bs4 import BeautifulSoup
import json


# # Отримання цитат та авторів

# authors.append(author)

# # Запис цитат у файл quotes.json

# # Запис авторів у файл authors.json
# unique_authors = list(set(authors))
# authors_data = [{'fullname': author} for author in unique_authors]

# with open('authors.json', 'w') as file:
#     json.dump(authors_data, file, indent=4)

# print("Скрапінг завершено. Дані збережені у файлах quotes.json та authors.json.")


def main():
    quotes = []
    authors = []
    links_for_authors = set()
    is_next = True
    base_url = 'http://quotes.toscrape.com'
    current_url = base_url
    while is_next:

        # Отримання HTML-сторінки
        response = requests.get(current_url)
        html = response.text

    # Парсинг HTML-сторінки з використанням BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        quote_elements = soup.select('.quote')

        for quote_element in quote_elements:
            text = quote_element.select_one('.text').text.strip()
            author = quote_element.select_one('.author').text
            tags = [tag.text for tag in quote_element.select('.tag')]

            quotes.append({'text': text, 'author': author, 'tags': tags})
            author_link = quote_element.find("a").get("href")
            links_for_authors.add(author_link)
            print(author_link)
            next_button = soup.find(class_="next")
            if next_button:
                next_button = next_button.find("a").get("href")
            print(next_button)
            if not next_button:
                is_next = False
            else:
                current_url = base_url + next_button
                print(current_url)
    with open('quotes.json', 'w') as file:
        json.dump(quotes, file, indent=4)
    print(links_for_authors)
    for author_url in links_for_authors:
        response = requests.get(base_url+author_url)
        html = response.text
    # Парсинг HTML-сторінки з використанням BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        full_name = soup.find(class_="author-title").text.strip()
        born_date = soup.find(class_="author-born-date").text.strip()
        born_location = soup.find(class_="author-born-location").text.strip()
        author_description = soup.find(
            class_="author-description").text.strip()
        authors.append({"full_name": full_name, "born_date": born_date,
                       "born_location": born_location, "author_description": author_description})
    with open('authors.json', 'w') as file:
        json.dump(authors, file, indent=4)
    print("Скрапінг завершено. Дані збережені в файлах quotes.json та authors.json.")


if __name__ == "__main__":
    main()
