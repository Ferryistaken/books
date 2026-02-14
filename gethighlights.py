#!/usr/bin/env python3

import csv
import os
import json
import requests

# URL of the Google Sheets CSV export
sheet_url = 'https://docs.google.com/spreadsheets/d/1n28Iqsj9nZL-ku6HOPJPSa6KUEpQ6xO00McQ96f2dww/export?exportFormat=csv'

# Attempt to download the CSV file
response = requests.get(sheet_url)
if response.status_code != 200:
    print("Failed to download the CSV file")
    exit(1)

# Decode the CSV data
csv_data = response.content.decode('utf-8')
csv_reader = csv.DictReader(csv_data.splitlines())

# Directories for storing data
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

# Dictionary to store book information
books = {}
# Dictionary to store non-ISBN sources and their highlights
non_isbn_sources = {}

# Function to check if a string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Process each row in the CSV
for row in csv_reader:
    isbn = row['isbn'].replace("-", "")
    highlight = row['highlight']

    # Check if ISBN is a number
    if is_number(isbn):
        # Handle rows with ISBN
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

        books[isbn]['highlights'].append(highlight)
    else:
        # Handle non-ISBN sources
        source = isbn if isbn.strip() else "Unknown Source"
        if source not in non_isbn_sources:
            non_isbn_sources[source] = []
        non_isbn_sources[source].append(highlight)

# Write information for each book to separate markdown files
for isbn, book in books.items():
    first_author = book['authors'][0].split()
    first_author_last_name = first_author[-1] if first_author else "Unknown"
    print(book)

    if book['title']=='Unknown Title':
        continue

    with open(os.path.join(collection_dir, f"{isbn}.md"), 'w', encoding='utf-8') as file:
        file.write('---\n')
        file.write('layout: books-post\n')
        file.write(f"title: \"{book['title']}\"\n")
        file.write(f"authors: \"{', '.join(book['authors'])}\"\n")
        file.write(f"first-author-last-name: \"{first_author_last_name}\"\n")
        file.write(f"publisher: \"{book['publisher']}\"\n")
        file.write(f"publishedDate: \"{book['publishedDate']}\"\n")
        file.write(f"page_number: \"{book['pageCount']}\"\n")
        file.write(f"coverImage: \"{book.get('coverImage', '')}\"\n")
        non_empty_highlights = [h for h in book['highlights'] if h.strip()]
        if non_empty_highlights:
            file.write('highlights:\n')
            for highlight in non_empty_highlights:
                highlight = highlight.replace('"', '\\"')
                file.write(f"  - \"{highlight}\"\n")

        file.write('---\n\n')

# if non_isbn_sources:
#     with open(os.path.join("other.md"), 'w', encoding='utf-8') as file:
#         file.write('---\n')
#         file.write('layout: other\n')
#         file.write('title: "Other Quotes"\n')
#         file.write('highlights:\n')
# 
#         for source, highlights in non_isbn_sources.items():
#             file.write(f"  - source: \"{source}\"\n")
#             file.write("    quotes:\n")
#             for highlight in highlights:
#                 highlight = highlight.replace('"', '\\"')
#                 file.write(f"      - \"{highlight}\"\n")
# 
#         file.write('---\n\n')
