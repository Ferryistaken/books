#!/usr/bin/env python3

import csv
import requests
import os
import json

def read_api_key(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().strip()

def get_book_info(isbn, api_key, cache):
    if isbn in cache:
        return cache[isbn]

    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            book_info = data["items"][0]["volumeInfo"]
            image_links = book_info.get('imageLinks', {})
            cover_image_url = image_links.get('thumbnail', '')

            book_data = {
                "title": book_info.get("title", "Unknown Title"),
                "authors": book_info.get("authors", ["Unknown Author"]),
                "publisher": book_info.get("publisher", "Unknown Publisher"),
                "publishedDate": book_info.get("publishedDate", "Unknown Date"),
                "coverImage": cover_image_url
            }
            cache[isbn] = book_data
            return book_data
    return None

api_key = os.environ.get("GOOGLE_API_KEY")
sheet_url = 'https://docs.google.com/spreadsheets/d/1n28Iqsj9nZL-ku6HOPJPSa6KUEpQ6xO00McQ96f2dww/export?exportFormat=csv'
response = requests.get(sheet_url)
if response.status_code != 200:
    print("Failed to download the CSV file")
    exit(1)

csv_reader = csv.DictReader(response.text.splitlines())
data_dir = '_data/books'
collection_dir = '_books'
os.makedirs(data_dir, exist_ok=True)
os.makedirs(collection_dir, exist_ok=True)

cache_file = 'books_cache.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as file:
        cache = json.load(file)
else:
    cache = {}

books = {}
for row in csv_reader:
    isbn = row['isbn']
    highlight = row['highlight']
    
    if isbn not in books:
        book_info = get_book_info(isbn, api_key, cache)
        if book_info:
            books[isbn] = book_info
            books[isbn]['highlights'] = []
    
    if isbn in books:
        books[isbn]['highlights'].append(highlight)

for isbn, book in books.items():
    with open(os.path.join(collection_dir, f"{isbn}.md"), 'w', encoding='utf-8') as file:
        file.write('---\n')
        file.write(f"title: \"{book['title']}\"\n")
        file.write(f"authors: \"{', '.join(book['authors'])}\"\n")
        file.write(f"publisher: \"{book['publisher']}\"\n")
        file.write(f"publishedDate: \"{book['publishedDate']}\"\n")
        file.write(f"coverImage: \"{book.get('coverImage', '')}\"\n")
        file.write('---\n\n')
        file.write(f"![Cover Image]({book['coverImage']})\n\n")
        file.write(f"# {book['title']}\n\n")
        file.write(f"**Author(s):** {', '.join(book['authors'])}\n\n")
        file.write(f"**Publisher:** {book['publisher']}\n\n")
        file.write(f"**Published Date:** {book['publishedDate']}\n\n")
        file.write('## Highlights\n<ul>\n')
        for highlight in book['highlights']:
            file.write(f"<li>{highlight}</li>\n")
        file.write('</ul>\n')

with open(cache_file, 'w', encoding='utf-8') as file:
    json.dump(cache, file, indent=4)
