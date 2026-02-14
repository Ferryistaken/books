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

echo "Build process finished."
