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

# Running Python scripts
python3 embeddings.py
print_success "embeddings.py executed."

python3 live-embeddings.py
print_success "live-embeddings.py executed."

python3 gethighlights.py
print_success "gethighlights.py executed."

# Building with Jekyll
bundle exec jekyll build
print_success "Jekyll build completed."

echo "Build process finished."
