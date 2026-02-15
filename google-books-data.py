#!/usr/bin/env python3

import csv
import requests
import json
import os
import sys

def fetch_and_cache_books_data(sheet_url, cache_file):
    response = requests.get(sheet_url)
    if response.status_code != 200:
        print("Failed to download the CSV file")
        exit(1)

    csv_data = response.content.decode('utf-8')
    csv_reader = csv.DictReader(csv_data.splitlines())

    unique_isbns = set()
    for row in csv_reader:
        if row['isbn'] == '':
            continue
        unique_isbns.add(int(row['isbn']))

    api_key = os.environ.get("GOOGLE_API_KEY")

    # Load existing cache if it exists
    cache = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as file:
                cache = json.load(file)
            print(f"Loaded {len(cache)} books from cache")
        except Exception as e:
            print(f"Warning: Could not load cache file: {e}")
            cache = {}

    google_calls = 0
    new_books = 0

    for isbn in unique_isbns:
        isbn_str = str(isbn)

        # Only query API if ISBN not already cached
        if isbn_str in cache:
            continue

        print(f"Fetching new book: {isbn}")
        book_data = get_book_info(isbn, api_key)
        google_calls += 1
        new_books += 1

        if book_data:
            cache[isbn_str] = book_data

    print(f"New books fetched: {new_books}")
    print(f"Total books in cache: {len(cache)}")
    print(f"TOTAL GOOGLE CALLS: {google_calls}")

    # Write cache back to file
    with open(cache_file, 'w', encoding='utf-8') as file:
        json.dump(cache, file, indent=4)

    return google_calls

def get_book_info(isbn, api_key):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            book_info = data["items"][0]["volumeInfo"]
            image_links = book_info.get('imageLinks', {})
            cover_image_url = image_links.get('thumbnail', '')

            return {
                "title": book_info.get("title", "Unknown Title"),
                "authors": book_info.get("authors", ["Unknown Author"]),
                "publisher": book_info.get("publisher", "Unknown Publisher"),
                "publishedDate": book_info.get("publishedDate", "Unknown Date"),
                "pageCount": book_info.get("pageCount", 250),
                "coverImage": cover_image_url
            }
    else:
        print("Couldn't Find Book", isbn)
        sys.exit(1)
        return None

if __name__ == "__main__":
    sheet_url = 'https://docs.google.com/spreadsheets/d/1n28Iqsj9nZL-ku6HOPJPSa6KUEpQ6xO00McQ96f2dww/export?exportFormat=csv'
    cache_file = 'books_cache.json'
    google_calls = fetch_and_cache_books_data(sheet_url, cache_file)
