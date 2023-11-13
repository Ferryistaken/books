#!/usr/bin/env python

import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

print("Generating DB")

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 256

# Read the CSV file
df = pd.read_csv('sheet.csv')

# Extract the sentences (highlights/quotes)
sentences = df['highlight'].tolist()

# Generate embeddings
embeddings = model.encode(sentences, normalize_embeddings=True)

# Convert embeddings to list for JSON compatibility
embeddings_list = embeddings.tolist()

# Save embeddings and sentences to a JSON file
data = {"sentences": sentences, "embeddings": embeddings_list}
with open("embeddings.json", "w") as file:
    json.dump(data, file)
