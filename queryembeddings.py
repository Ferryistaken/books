#!/usr/bin/env python

print("Import libraries")

import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

print("Building database")

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 256

# Read the CSV file
df = pd.read_csv('sheet.csv')

# Extract the sentences (highlights/quotes)
sentences = df['highlight'].tolist()

# Encode the sentences to get embeddings
document_embeddings = model.encode(sentences, normalize_embeddings=True)

# Let's say we have a query
query = input("Query: ")
query_embedding = model.encode(query, normalize_embeddings=True)

# Calculate cosine similarities
cosine_scores = util.pytorch_cos_sim(query_embedding, document_embeddings)

# Rank the sentences
top_results = torch.topk(cosine_scores, k=5)

print("Query:", query)
print("\nTop 5 most similar sentences in corpus:")
for score, idx in zip(top_results[0][0], top_results[1][0]):
    print(sentences[idx], "(Score: {:.4f})".format(score))
    print()
