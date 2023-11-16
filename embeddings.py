import pandas as pd
from sentence_transformers import SentenceTransformer
import json

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 256

# Read the CSV file
df = pd.read_csv('sheet.csv')

# Group by ISBN and create indices within each group
df['index'] = df.groupby('isbn').cumcount()

# Extract sentences (highlights/quotes), ISBNs, and indices
sentences = df['highlight'].tolist()
isbns = df['isbn'].tolist()
indices = df['index'].tolist()

# Generate embeddings
embeddings = model.encode(sentences, normalize_embeddings=True)

# Convert embeddings to list for JSON compatibility
embeddings_list = embeddings.tolist()

# Save embeddings, sentences, ISBNs, and indices to a JSON file
data = {
    "sentences": sentences,
    "embeddings": embeddings_list,
    "isbns": isbns,
    "indices": indices
}

with open("embeddings.json", "w") as file:
    json.dump(data, file)
