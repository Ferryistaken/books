const fs = require('fs');
const path = require('path');
const math = require('mathjs');
import { pipeline } from '@xenova/transformers';

exports.handler = async (event) => {
    // URL of the embeddings JSON file
    const embeddingsUrl = '<url>/embeddings.json';

    // Fetch the embeddings data from the URL
    const response = await fetch(embeddingsUrl);
    const data = await response.json();

    const sentences = data.sentences;
    const embeddings = data.embeddings;

    // Extract query from event
    const query = event.queryStringParameters.q;

    // Initialize the feature extraction pipeline
    let extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

    // Calculate query embedding
    const queryEmbeddingOutput = await extractor(query, { pooling: 'mean', normalize: true });
    const queryEmbedding = queryEmbeddingOutput[0]; // Extract the embedding

    // Calculate similarities
    let scores = embeddings.map(embedding => {
        return math.dot(queryEmbedding, embedding) / 
               (math.norm(queryEmbedding) * math.norm(embedding));
    });

    // Find top results
    let indices = scores.map((score, index) => [score, index]);
    indices.sort((a, b) => b[0] - a[0]);
    let topResults = indices.slice(0, 5);

    // Prepare response
    const results = topResults.map(item => sentences[item[1]]);

    return {
        statusCode: 200,
        body: JSON.stringify(results)
    };
};
