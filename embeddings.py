import pandas as pd
from sentence_transformers import SentenceTransformer
import json
import umap.umap_ as umap
import matplotlib.pyplot as plt
import numpy as np
import requests
import os

def get_book_title(isbn):
    api_key = os.environ.get('GOOGLE_API_KEY')
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        return "Title Not Found"

    data = response.json()
    if "items" in data:
        try:
            title = data["items"][0]["volumeInfo"]["title"]
            return title
        except (IndexError, KeyError):
            return "Title Not Found"
    else:
        return "Title Not Found"

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 256

# Read the CSV file
df = pd.read_csv('sheet.csv')

# Maintain the original 'index' column
df['original_index'] = df.index

# Group by ISBN and create indices within each group
df['group_index'] = df.groupby('isbn').cumcount()

# Extract sentences (highlights/quotes), ISBNs, and group indices
sentences = df['highlight'].tolist()
isbns = df['isbn'].tolist()
group_indices = df['group_index'].tolist()

# Generate embeddings
embeddings = model.encode(sentences, normalize_embeddings=True)

# Convert embeddings to list for JSON compatibility and save to JSON
embeddings_list = embeddings.tolist()
data = {
    "sentences": sentences, 
    "embeddings": embeddings_list, 
    "isbns": isbns, 
    "group_indices": group_indices
}
with open("embeddings.json", "w") as file:
    json.dump(data, file)

# Dimensionality reduction using UMAP
umap_embeddings = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine').fit_transform(embeddings)

markers = ['o', 's', '^', 'D', '*', 'x', '+', '>', '<', 'p', 'h', 'H', 'X', 'd']

# Creating a color map and fetching titles for each unique ISBN
unique_isbns = list(set(isbns))
isbn_to_title = {isbn: get_book_title(isbn) for isbn in unique_isbns}
colors = plt.cm.jet(np.linspace(0, 1, len(unique_isbns)))
isbn_to_color = {isbn: color for isbn, color in zip(unique_isbns, colors)}

# Plotting
plt.figure(figsize=(12,10))
for idx, isbn in enumerate(unique_isbns):
    indices = [i for i, x in enumerate(isbns) if x == isbn]
    marker_style = markers[idx % len(markers)]  # Cycle through markers
    plt.scatter(umap_embeddings[indices, 0], umap_embeddings[indices, 1], s=20, color=isbn_to_color[isbn], label=isbn_to_title[isbn], marker=marker_style)

plt.title('Embeddings Visualization using UMAP')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.legend(title='Book Title', bbox_to_anchor=(1.05, 1), loc='upper left')

# Save the plot as a PNG file
plt.savefig("umap.png", dpi=300, bbox_inches='tight')

