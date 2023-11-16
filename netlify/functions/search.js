const math = require('mathjs');

let pipeline;

(async () => {
  const transformers = await import('@xenova/transformers');
  pipeline = transformers.pipeline;
})();

exports.handler = async (event) => {
    // URL of the embeddings JSON file
    const embeddingsUrl = 'https://books.alessandroferrari.live/embeddings.json';

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

    const arrayQueryEmbedding = Array.from(queryEmbedding.data);

    console.log(arrayQueryEmbedding);
    //console.log(embeddings.every(embedding => Array.isArray(embedding))); // Should also be true


    // Calculate similarities
    let scores = embeddings.map(embedding => {
        return math.dot(arrayQueryEmbedding, embedding) / 
               (math.norm(arrayQueryEmbedding) * math.norm(embedding));
    });

    // Find top results
    let indices = scores.map((score, index) => [score, index]);
    indices.sort((a, b) => b[0] - a[0]);
    let topResults = indices.slice(0, 5);

    // Prepare response
    const results = topResults.map(item => {
        return {
            sentence: sentences[item[1]],
            similarity: item[0]  // Add the similarity score
        };
    });

    return {
        statusCode: 200,
        body: JSON.stringify(results)
    };

};
