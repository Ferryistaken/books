const math = require('mathjs');

exports.handler = async (event) => {
    const transformers = await import('@xenova/transformers');
    const pipeline = transformers.pipeline;
    // URL of the embeddings JSON file
    const embeddingsUrl = 'https://books.alessandroferrari.live/embeddings.json';
    //const embeddingsUrl = 'http://localhost:8888/embeddings.json';

    // Fetch the embeddings data from the URL
    const response = await fetch(embeddingsUrl);
    const data = await response.json();

    const sentences = data.sentences;
    const embeddings = data.embeddings;
    const isbns = data.isbns; // Include the ISBNs
    const indexes = data.group_indices;
    const titles = data.titles;
    const authors = data.authors;

    console.log(titles);
    console.log(authors);

    // Extract query from event
    const query = event.queryStringParameters.q;

    // Initialize the feature extraction pipeline - multilingual for Italian + English
    let extractor = await pipeline('feature-extraction', 'Xenova/multilingual-e5-small');

    // Calculate query embedding
    const queryEmbeddingOutput = await extractor(query, { pooling: 'mean', normalize: true });
    const queryEmbedding = queryEmbeddingOutput[0]; // Extract the embedding

    const arrayQueryEmbedding = Array.from(queryEmbedding.data);

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
            similarity: item[0],  // Add the similarity score
            isbn: isbns[item[1]], // Include the ISBN
            index: indexes[item[1]],
            author: authors[item[1]],
            title: titles[item[1]],
        };
    });

    return {
        statusCode: 200,
        body: JSON.stringify(results)
    };

};
