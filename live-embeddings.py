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

# Load data from embeddings.json
with open("embeddings.json", "r") as file:
    data = json.load(file)

print("- ✅ Data loaded from 'embeddings.json'")

# Load cached book data
with open("books_cache.json", "r") as file:
    cached_data = json.load(file)

embeddings = np.array(data["embeddings"])
sentences = data["sentences"]
isbns = data["isbns"]

# Dimensionality reduction using UMAP
umap_embeddings = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine').fit_transform(embeddings)

print("- ✅ Created UMAP")


# Use cached data for titles
isbn_to_title = {}
for isbn in isbns:
    isbn = str(isbn)
    if isbn in cached_data:
        title = cached_data[isbn]["title"]
    else:
        title = "Title Not Found"
        print(isbn, "not found")
        print(cached_data)
    isbn_to_title[isbn] = title

unique_isbns = list(set(isbns))
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
    f"<b><i>{isbn_to_title[str(isbn)].upper()}</i></b><br><br>" + '<br>'.join(textwrap.wrap(str(sentence), width=80))
    for sentence, url, isbn in zip(sentences, urls, isbns)
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
        text=isbn_data['text'],
        hoverinfo='text',
        name=isbn_to_title[str(isbn)]
    ))

# Update layout
fig.update_layout(
    title='',
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent to adapt to theme
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
)

# Save the figure as an HTML file
config = {'displayModeBar': False, 'scrollZoom': False}
fig.write_html("plotly-out.html", config=config)

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
        name=isbn_to_title[str(isbn)]
    ))

# Update layout for square plot without legend
squareFig.update_layout(
    title='',
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent to inherit page background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
    showlegend=False,  # Disable the legend
    autosize=False,    # Disable autosizing
    width=450,         # Width of the plot
    height=450,        # Height of the plot (same as width for square)
    margin=dict(       # Minimal margins for cleaner look
        l=0,           # Left margin
        r=0,           # Right margin
        b=0,           # Bottom margin
        t=0,           # Top margin
        pad=0          # Padding
    )
)

# Save the squareFigure as an HTML file with a new name and configure to prevent scrollbars
config = {
    'displayModeBar': False,  # Hide the mode bar
    'scrollZoom': False,      # Disable scroll zoom
    'staticPlot': False       # Keep interactive (hover) but no zoom/pan
}
squareFig.write_html("square-plot.html", config=config)

print("- ✅ Plotted Second Figure")
