#!/usr/bin/env python

print("Loading libraries")

import pandas as pd
from sentence_transformers import SentenceTransformer
import json
import umap.umap_ as umap
from adjustText import adjust_text
import matplotlib.pyplot as plt
import numpy as np
import requests
import os

print("Loading Model")

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 256

print("Loading data")

# Read the CSV file
df = pd.read_csv('sheet.csv')

# Load cached book data
with open("books_cache.json", "r") as file:
    isbn_to_info = json.load(file)

df['highlight'] = df['highlight'].astype(str).str.strip()

# Remove rows with NaN or empty strings in 'highlight'
df = df[(df['highlight'].str.lower() != 'nan') & (df['highlight'] != '')]

# If there are no valid rows left, exit the script
if df.empty:
    print("No data to process")
    exit(0)

# Group the DataFrame by ISBN and filter out groups with no valid highlights
df = df.groupby('isbn').filter(lambda x: x['highlight'].str.strip().astype(bool).any())

# If there are no books with valid highlights, exit the script
if df.empty:
    print("No books with valid highlights to process")
    exit(0)

# Reset index after filtering
df.reset_index(drop=True, inplace=True)

# Maintain the original 'index' column
df['original_index'] = df.index

# Group by ISBN and create indices within each group
df['group_index'] = df.groupby('isbn').cumcount()

# Extract sentences (highlights/quotes), ISBNs, and group indices
sentences = df['highlight'].astype(str).tolist()  # Convert highlights to strings
isbns = df['isbn'].tolist()
group_indices = df['group_index'].tolist()

# Create arrays for titles and authors
titles = [isbn_to_info[isbn]["title"] if isbn in isbn_to_info else "Title Not Found" for isbn in isbns]
authors = [', '.join(isbn_to_info[isbn]["authors"]) if isbn in isbn_to_info else "Author Not Found" for isbn in isbns]

print("Encoding data")

# Generate embeddings
try:
    embeddings = model.encode(sentences, normalize_embeddings=True)
except Exception as e:
    print(f"Error during encoding: {e}")
    exit(1)

# Convert embeddings to list for JSON compatibility and save to JSON
embeddings_list = embeddings.tolist()
data = {
    "sentences": sentences, 
    "embeddings": embeddings_list, 
    "isbns": isbns, 
    "group_indices": group_indices,
    "titles": titles,  # Add the book titles
    "authors": authors  # Add the authors
}

print("Saving embeddings")

with open("embeddings.json", "w") as file:
    json.dump(data, file)

print("Generating visualization")

# Dimensionality reduction using UMAP
umap_embeddings = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine').fit_transform(embeddings)

markers = ['o', 's', '^', 'D', '*', 'x', '+', '>', '<', 'p', 'h', 'H', 'X', 'd']

colors = plt.cm.jet(np.linspace(0, 1, len(unique_isbns)))
isbn_to_color = {isbn: color for isbn, color in zip(unique_isbns, colors)}

plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

# Plotting
plt.figure(figsize=(12,10))
legend_elements = []
texts = []  # List to store all the texts for adjust_text

for idx, isbn in enumerate(unique_isbns):
    indices = [i for i, x in enumerate(isbns) if x == isbn]
    marker_style = markers[idx % len(markers)]  # Cycle through markers

    # Scatter plot
    scatter = plt.scatter(umap_embeddings[indices, 0], umap_embeddings[indices, 1], s=30, color=isbn_to_color[isbn], marker=marker_style)

    # Calculating centroid of each cluster
    centroid_x = np.mean(umap_embeddings[indices, 0])
    centroid_y = np.mean(umap_embeddings[indices, 1])

    title = isbn_to_info[isbn]["title"] if isbn in isbn_to_info else "Title Not Found"
    authors = ', '.join(isbn_to_info[isbn]["authors"]) if isbn in isbn_to_info else "Author Not Found"
    book_label = f"{title} by {authors}"
    text = plt.text(centroid_x, centroid_y, book_label, fontsize=8, ha='center', va='center', color='white')
    texts.append(text)
    legend_elements.append(plt.Line2D([0], [0], marker=marker_style, color='w', label=book_label, markersize=10, markerfacecolor=scatter.get_facecolor()[0], linestyle='None'))

plt.legend(handles=legend_elements, title='Books', bbox_to_anchor=(1.05, 1), loc='upper left')

# Use adjust_text to iteratively adjust text position
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))

plt.title('Vector Space (UMAP)', fontsize=20)
plt.grid(False)
plt.axis('off')

# Save the plot as a PNG file
plt.savefig("umap.png", dpi=300, bbox_inches='tight')

