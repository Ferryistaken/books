#!/usr/bin/env python3

import csv
import os
import json

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

# Load cached book data
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
        book_info = cache.get(isbn, {
            "title": "Unknown Title",
            "authors": ["Unknown Author"],
            "publisher": "Unknown Publisher",
            "publishedDate": "Unknown Date",
            "coverImage": ""
        })
        books[isbn] = book_info
        books[isbn]['highlights'] = []

    if isbn in books:
        books[isbn]['highlights'].append(highlight)

for isbn, book in books.items():
    first_author = book['authors'][0].split()
    first_author_last_name = first_author[-1] if first_author else "Unknown"

    with open(os.path.join(collection_dir, f"{isbn}.md"), 'w', encoding='utf-8') as file:
        file.write('---\n')
        file.write('layout: post\n')
        file.write(f"title: \"{book['title']}\"\n")
        file.write(f"authors: \"{', '.join(book['authors'])}\"\n")
        file.write(f"first-author-last-name: \"{first_author_last_name}\"\n")
        file.write(f"publisher: \"{book['publisher']}\"\n")
        file.write(f"publishedDate: \"{book['publishedDate']}\"\n")
        file.write(f"coverImage: \"{book.get('coverImage', '')}\"\n")

        # Check if there are any non-empty highlights
        non_empty_highlights = [h for h in book['highlights'] if h.strip()]
        if non_empty_highlights:
            file.write('highlights:\n')
            for highlight in non_empty_highlights:
                highlight = highlight.replace('"', '\\"')
                file.write(f"  - \"{highlight}\"\n")

        file.write('---\n\n')
