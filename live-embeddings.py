#!/usr/bin/env python

import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import umap.umap_ as umap
import numpy as np
import os
import requests
import textwrap

print("- ✅ Loaded libraries")

# Function to fetch book titles using Google Books API
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

# Load data from embeddings.json
with open("embeddings.json", "r") as file:
    data = json.load(file)

print("- ✅ Data loaded from 'embeddings.json'")

embeddings = np.array(data["embeddings"])
sentences = data["sentences"]
isbns = data["isbns"]

# Dimensionality reduction using UMAP
umap_embeddings = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine').fit_transform(embeddings)

print("- ✅ Created UMAP")

# Get unique ISBNs and their corresponding titles
unique_isbns = list(set(isbns))
isbn_to_title = {isbn: get_book_title(isbn) for isbn in unique_isbns}
colors = px.colors.qualitative.Plotly

highlight_ids = {isbn: 0 for isbn in unique_isbns}

# Function to generate URL and update highlight IDs
def generate_url(isbn):
    url = f"https://books.alessandroferrari.live/{isbn}#{highlight_ids[isbn]}"
    highlight_ids[isbn] += 1
    return url

# Generate URLs for each highlight
urls = [generate_url(isbn) for isbn in isbns]

# Wrap text for each highlight and append URL
wrapped_sentences_with_url = [
    '<br>'.join(textwrap.wrap(str(sentence), width=80)) + f"<br>URL: {url}" 
    for sentence, url in zip(sentences, urls)
]

# Prepare Plotly data
plot_data = pd.DataFrame({
    'x': umap_embeddings[:, 0],
    'y': umap_embeddings[:, 1],
    'text': wrapped_sentences_with_url,
    'isbn': isbns
})


# Create Plotly figure
fig = go.Figure()

for idx, isbn in enumerate(unique_isbns):
    isbn_data = plot_data[plot_data['isbn'] == isbn]
    fig.add_trace(go.Scatter(
        x=isbn_data['x'],
        y=isbn_data['y'],
        mode='markers',
        marker=dict(color=colors[idx % len(colors)], size=10),
        text=isbn_data['text'],  # Include the wrapped text with URL
        hoverinfo='text',       # Only show the text on hover
        name=isbn_to_title[isbn]
    ))

# Update layout
fig.update_layout(
    title='',
    plot_bgcolor='white',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
)

# Save the figure as an HTML file
fig.write_html("plotly-out.html")

print("- ✅ Plotted first figure")

squareFig = go.Figure()

for idx, isbn in enumerate(unique_isbns):
    isbn_data = plot_data[plot_data['isbn'] == isbn]
    squareFig.add_trace(go.Scatter(
        x=isbn_data['x'],
        y=isbn_data['y'],
        mode='markers',
        marker=dict(color=colors[idx % len(colors)], size=10),
        text=isbn_data['text'],  # Include the wrapped text with URL
        hoverinfo='text',       # Only show the text on hover
        name=isbn_to_title[isbn]
    ))

# Update layout for square plot without legend
squareFig.update_layout(
    title='',
    plot_bgcolor='white',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    showlegend=False,  # Disable the legend
    autosize=False,    # Disable autosizing
    width=350,         # Width of the plot
    height=350,         # Height of the plot (same as width for square)
    margin=dict(       # Adjust margins to fit in an iframe without scrollbars
        l=100,           # Left margin
        r=0,           # Right margin
        b=0,           # Bottom margin
        t=0,           # Top margin
        pad=0          # Padding
    )
)

# Save the squareFigure as an HTML file with a new name
squareFig.write_html("square-plot.html")

print("- ✅ Plotted Second Figure")
