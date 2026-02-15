#!/bin/bash

# Stop on first error
set -e

# Function to print a success message with a green check mark
print_success() {
    # Using ANSI escape codes for green color
    echo -e "\e[32m✅ $1\e[0m"
}

echo "Starting build process..."

# Create cache directories
mkdir -p ~/.cache/sentence_transformers
mkdir -p /opt/build/cache/books

# Restore cached files from Netlify's cache directory
if [ -f /opt/build/cache/books/books_cache.json ]; then
    cp /opt/build/cache/books/books_cache.json ./books_cache.json
    print_success "Restored books_cache.json from Netlify cache"
fi

if [ -f /opt/build/cache/books/.embeddings_cache_hash ]; then
    cp /opt/build/cache/books/.embeddings_cache_hash ./.embeddings_cache_hash
fi

if [ -f /opt/build/cache/books/embeddings.json ]; then
    cp /opt/build/cache/books/embeddings.json ./embeddings.json
fi

if [ -f /opt/build/cache/books/umap.png ]; then
    cp /opt/build/cache/books/umap.png ./umap.png
fi

# Downloading data
curl -L $SHEET_URL -o sheet.csv
print_success "Data downloaded."

python3 google-books-data.py
print_success "Google API Queried"

# Running Python scripts - embeddings.py now has smart caching
python3 embeddings.py
print_success "embeddings.py executed."

# These can run in parallel as they're independent
python3 live-embeddings.py &
LIVE_EMB_PID=$!
python3 gethighlights.py &
HIGHLIGHTS_PID=$!

# Wait for both to complete
wait $LIVE_EMB_PID
print_success "live-embeddings.py executed."
wait $HIGHLIGHTS_PID
print_success "gethighlights.py executed."

# Installing Jekyll dependencies
bundle install
print_success "Bundle install completed."

# Building with Jekyll
bundle exec jekyll build
workbox generateSW workbox-config.js
print_success "Jekyll build completed."

# Save files to Netlify cache for next build
cp books_cache.json /opt/build/cache/books/books_cache.json 2>/dev/null || true
cp .embeddings_cache_hash /opt/build/cache/books/.embeddings_cache_hash 2>/dev/null || true
cp embeddings.json /opt/build/cache/books/embeddings.json 2>/dev/null || true
cp umap.png /opt/build/cache/books/umap.png 2>/dev/null || true
print_success "Cached files for next build"

echo "Build process finished."
