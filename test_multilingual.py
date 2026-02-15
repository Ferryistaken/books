#!/usr/bin/env python3
"""
Test script to compare old (all-MiniLM-L6-v2) vs new (multilingual-e5-small) models
"""

import numpy as np
from sentence_transformers import SentenceTransformer, util

print("=" * 80)
print("EMBEDDING MODEL COMPARISON TEST")
print("=" * 80)
print()

# Test sentences - mix of English and Italian
test_sentences = [
    # English philosophical quotes
    "The unexamined life is not worth living.",
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
    "Death is nothing to fear, for the fear of death is what we should fear.",

    # Italian philosophical quotes (similar meanings)
    "La vita senza ricerca non è degna di essere vissuta.",  # The unexamined life is not worth living
    "Siamo ciò che facciamo ripetutamente. L'eccellenza non è un atto, ma un'abitudine.",  # We are what we repeatedly do
    "La morte non è nulla da temere, è la paura della morte che dobbiamo temere.",  # Death is nothing to fear

    # English stoic quotes
    "The obstacle is the way.",
    "You have power over your mind, not outside events.",

    # Italian stoic quotes
    "L'ostacolo è la via.",  # The obstacle is the way
    "Hai potere sulla tua mente, non sugli eventi esterni.",  # You have power over your mind
]

print("Test sentences:")
for i, sent in enumerate(test_sentences, 1):
    print(f"{i}. {sent}")
print()

# Test queries
test_queries = [
    ("English: philosophy", "philosophy of life"),
    ("English: stoicism", "stoic philosophy and mind control"),
    ("Italian: filosofia", "filosofia della vita"),
    ("Italian: stoicismo", "filosofia stoica e controllo della mente"),
]

print("=" * 80)
print("Loading models...")
print("=" * 80)

# Old model (English only)
print("\n1. Loading all-MiniLM-L6-v2 (English only)...")
old_model = SentenceTransformer("all-MiniLM-L6-v2")
old_model.max_seq_length = 256

# New model (Multilingual)
print("2. Loading intfloat/multilingual-e5-small (100+ languages)...")
new_model = SentenceTransformer("intfloat/multilingual-e5-small")
new_model.max_seq_length = 256

print("\nGenerating embeddings...")
old_embeddings = old_model.encode(test_sentences, normalize_embeddings=True)
new_embeddings = new_model.encode(test_sentences, normalize_embeddings=True)

print("\n" + "=" * 80)
print("SEARCH QUALITY COMPARISON")
print("=" * 80)

for query_label, query_text in test_queries:
    print(f"\n{'─' * 80}")
    print(f"Query [{query_label}]: \"{query_text}\"")
    print("─" * 80)

    # Old model results
    old_query_emb = old_model.encode(query_text, normalize_embeddings=True)
    old_scores = util.pytorch_cos_sim(old_query_emb, old_embeddings)[0]
    old_top3 = old_scores.argsort(descending=True)[:3]

    # New model results
    new_query_emb = new_model.encode(query_text, normalize_embeddings=True)
    new_scores = util.pytorch_cos_sim(new_query_emb, new_embeddings)[0]
    new_top3 = new_scores.argsort(descending=True)[:3]

    print("\n🔴 OLD MODEL (all-MiniLM-L6-v2 - English only):")
    for i, idx in enumerate(old_top3, 1):
        score = old_scores[idx].item()
        sentence = test_sentences[idx]
        lang = "🇬🇧" if idx < 3 or (idx >= 6 and idx < 8) else "🇮🇹"
        print(f"  {i}. [{score:.3f}] {lang} {sentence}")

    print("\n🟢 NEW MODEL (multilingual-e5-small - 100+ languages):")
    for i, idx in enumerate(new_top3, 1):
        score = new_scores[idx].item()
        sentence = test_sentences[idx]
        lang = "🇬🇧" if idx < 3 or (idx >= 6 and idx < 8) else "🇮🇹"
        print(f"  {i}. [{score:.3f}] {lang} {sentence}")

print("\n" + "=" * 80)
print("EMBEDDING SPACE ANALYSIS")
print("=" * 80)

# Calculate average similarity within English vs Italian for both models
en_indices = [0, 1, 2, 6, 7]  # English quotes
it_indices = [3, 4, 5, 8, 9]  # Italian quotes

def avg_similarity(embeddings, indices):
    """Calculate average cosine similarity within a group"""
    sims = []
    for i in range(len(indices)):
        for j in range(i+1, len(indices)):
            sim = np.dot(embeddings[indices[i]], embeddings[indices[j]])
            sims.append(sim)
    return np.mean(sims) if sims else 0

def cross_similarity(embeddings, indices1, indices2):
    """Calculate average similarity between two groups"""
    sims = []
    for i in indices1:
        for j in indices2:
            sim = np.dot(embeddings[i], embeddings[j])
            sims.append(sim)
    return np.mean(sims) if sims else 0

print("\n🔴 OLD MODEL:")
old_en_sim = avg_similarity(old_embeddings, en_indices)
old_it_sim = avg_similarity(old_embeddings, it_indices)
old_cross_sim = cross_similarity(old_embeddings, en_indices, it_indices)
print(f"  English-English similarity: {old_en_sim:.3f}")
print(f"  Italian-Italian similarity: {old_it_sim:.3f}")
print(f"  English-Italian similarity: {old_cross_sim:.3f}")
print(f"  Separation score: {(old_en_sim + old_it_sim) / 2 - old_cross_sim:.3f} (higher = more separated)")

print("\n🟢 NEW MODEL:")
new_en_sim = avg_similarity(new_embeddings, en_indices)
new_it_sim = avg_similarity(new_embeddings, it_indices)
new_cross_sim = cross_similarity(new_embeddings, en_indices, it_indices)
print(f"  English-English similarity: {new_en_sim:.3f}")
print(f"  Italian-Italian similarity: {new_it_sim:.3f}")
print(f"  English-Italian similarity: {new_cross_sim:.3f}")
print(f"  Separation score: {(new_en_sim + new_it_sim) / 2 - new_cross_sim:.3f} (lower = better cross-lingual)")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)
print()
print("✅ The multilingual model should show:")
print("   1. Better matching for Italian queries (higher scores for Italian results)")
print("   2. Better cross-lingual understanding (similar English/Italian quotes cluster)")
print("   3. Higher English-Italian similarity (understands semantic meaning across languages)")
print()
print("❌ The old model will show:")
print("   1. Poor Italian matching (treats Italian as random characters)")
print("   2. Latent space collapse for Italian (all Italian quotes cluster separately)")
print("   3. Lower cross-lingual similarity (can't relate English and Italian)")
print()
print("=" * 80)
