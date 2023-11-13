const fs = require('fs');
const path = require('path');
const math = require('mathjs');

exports.handler = async (event) => {
    // Load embeddings data
    let data = fs.readFileSync(path.join(__dirname, '../embeddings.json'));
    data = JSON.parse(data);

    const sentences = data.sentences;
    const embeddings = data.embeddings;

    // Extract query from event
    const query = event.queryStringParameters.q;

    // Calculate query embedding - this part depends on how you implement it in JS
    const queryEmbedding = ...; // You need to define this part

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
