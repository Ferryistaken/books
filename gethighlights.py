#!/usr/bin/env python3

import csv
import requests
import os
import json
import hashlib

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
    else:
        print("Couldn't Find Book", isbn)
        return None

api_key = os.environ.get("GOOGLE_API_KEY")
sheet_url = 'https://docs.google.com/spreadsheets/d/1n28Iqsj9nZL-ku6HOPJPSa6KUEpQ6xO00McQ96f2dww/export?exportFormat=csv'

response = requests.get(sheet_url)
if response.status_code != 200:
    print("Failed to download the CSV file")
    exit(1)

csv_data = response.content.decode('utf-8')
csv_reader = csv.DictReader(csv_data.splitlines())
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
    # print(highlight)
    # print("Finding ", isbn)

    if isbn not in books:
        # print("Fetching", isbn)
        book_info = get_book_info(isbn, api_key, cache)
        if book_info:
            books[isbn] = book_info
            books[isbn]['highlights'] = []

    if isbn in books:
        books[isbn]['highlights'].append(highlight)

for isbn, book in books.items():
    with open(os.path.join(collection_dir, f"{isbn}.md"), 'w', encoding='utf-8') as file:
        file.write('---\n')
        file.write(f"layout: post\n")
        file.write(f"title: \"{book['title']}\"\n")
        file.write(f"authors: \"{', '.join(book['authors'])}\"\n")
        file.write("tags: [")
        file.write(', '.join([f'{author}' for author in book['authors']]))
        file.write("]\n")
        file.write(f"publisher: \"{book['publisher']}\"\n")
        file.write(f"publishedDate: \"{book['publishedDate']}\"\n")
        file.write(f"coverImage: \"{book.get('coverImage', '')}\"\n")
        file.write('---\n\n')
        alt_text = book['title'].replace("'", "’").replace('"', "“")
        # Center and enlarge the cover image
        file.write(f"<div style='text-align: center;'>\n")
        alt_text = book['title'].replace("'", "’").replace('"', "“")
        file.write(f"  <img src='{book['coverImage']}' alt='{alt_text}' style='max-width: 80%;'>\n")
        file.write(f"</div>\n\n")
        file.write(f"<h2 style='text-align: center; font-weight: bold; font-size: 24px;'>{book['title']}</h2>\n\n")
        # Center the authors without label and add only the year
        file.write(f"<p style='text-align: center;'>{', '.join(book['authors'])}<br>{book['publishedDate'].split('-')[0]}</p>\n\n")
        file.write('## Highlights\n')
        file.write('<div style="text-align: center;">\n')
        file.write('  <ul style="list-style-type: none; padding: 0;">\n')
        for index, highlight in enumerate(book['highlights']):
            highlight_id = f"{index}"
            full_url = f"https://books.alessandroferrari.live/books/{isbn}.html#{highlight_id}"
            # highlight = highlight.replace("'", "’").replace('"', "“")
            # print(highlight)
            # Apply highlight styling to the text only
            file.write(f'    <li id="{highlight_id}" style="font-size: 18px; margin-bottom: 10px; padding: 0;">'
                       f'<span style="background-color: rgba(255, 226, 130, 0.5); padding: 2px;">{highlight}</span>'
                       f'<br>'  # Add a newline (line break)
                       f'<em>—{book["title"]}</em> by {", ".join(book["authors"])}'
                       f' <a href="{full_url}" target="_blank">[Link]</a>'
                       f'</li>\n')
        file.write('  </ul>\n')
        file.write('</div>\n')
        file.write('<br>\n')
        file.write('<br>\n')

with open(cache_file, 'w', encoding='utf-8') as file:
    json.dump(cache, file, indent=4)
