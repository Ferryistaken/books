#!/bin/bash

# Stop on first error
set -e

# Function to print a success message with a green check mark
print_success() {
    # Using ANSI escape codes for green color
    echo -e "\e[32m✅ $1\e[0m"
}

echo "Starting build process..."


# Downloading data
curl -L $SHEET_URL -o sheet.csv
print_success "Data downloaded."

python3 google-books-data.py
print_success "Google API Queried"

# Running Python scripts in parallel where possible
python3 embeddings.py &
EMBED_PID=$!
python3 gethighlights.py &
HIGHLIGHTS_PID=$!

# Wait for both to complete
wait $EMBED_PID
print_success "embeddings.py executed."
wait $HIGHLIGHTS_PID
print_success "gethighlights.py executed."

# This depends on embeddings.py output
python3 live-embeddings.py
print_success "live-embeddings.py executed."

# Installing Jekyll dependencies
bundle install
print_success "Bundle install completed."

# Building with Jekyll
bundle exec jekyll build
workbox generateSW workbox-config.js
print_success "Jekyll build completed."

echo "Build process finished."
