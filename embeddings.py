print("Loading libraries")

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

print("Loading Model")

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 256

print("Loading data")

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

print("Encoding data")

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

print("Saving embeddings")

with open("embeddings.json", "w") as file:
    json.dump(data, file)

print("Generating visualization")

# Dimensionality reduction using UMAP
umap_embeddings = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine').fit_transform(embeddings)

markers = ['o', 's', '^', 'D', '*', 'x', '+', '>', '<', 'p', 'h', 'H', 'X', 'd']

# Creating a color map and fetching titles for each unique ISBN
unique_isbns = list(set(isbns))
isbn_to_title = {isbn: get_book_title(isbn) for isbn in unique_isbns}
colors = plt.cm.jet(np.linspace(0, 1, len(unique_isbns)))
isbn_to_color = {isbn: color for isbn, color in zip(unique_isbns, colors)}

plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

# Plotting
plt.figure(figsize=(12,10))
legend_elements = []

for idx, isbn in enumerate(unique_isbns):
    indices = [i for i, x in enumerate(isbns) if x == isbn]
    marker_style = markers[idx % len(markers)]  # Cycle through markers

    # Scatter plot
    scatter = plt.scatter(umap_embeddings[indices, 0], umap_embeddings[indices, 1], s=30, color=isbn_to_color[isbn], marker=marker_style)

    # Calculating centroid of each cluster
    centroid_x = np.mean(umap_embeddings[indices, 0])
    centroid_y = np.mean(umap_embeddings[indices, 1])

    # Annotate with book title at the centroid
    plt.annotate(isbn_to_title[isbn], (centroid_x, centroid_y), fontsize=9, ha='center', va='center', color='white')

    # Create a custom legend entry for each ISBN
    legend_elements.append(plt.Line2D([0], [0], marker=marker_style, color='w', label=isbn_to_title[isbn], markersize=10, markerfacecolor=scatter.get_facecolor()[0], linestyle='None'))

plt.title('Vector Space (UMAP)', fontsize=20)

# Add a legend and adjust its properties
legend = plt.legend(handles=legend_elements, title='', loc='upper right', bbox_to_anchor=(1, 0.9), bbox_transform=plt.gcf().transFigure)
legend.get_frame().set_alpha(0.5)  # Adjust the opacity

plt.grid(False)
plt.axis('off')

# Save the plot as a PNG file
plt.savefig("umap.png", dpi=300, bbox_inches='tight')
