[![Netlify Status](https://api.netlify.com/api/v1/badges/2423e3e6-52d9-40e1-940a-0276913477e1/deploy-status)](https://app.netlify.com/sites/comfy-bunny-349a79/deploys)

<img src="https://alessandroferrari.live/assets/posts/book-highlights/book-highlight-diagram.png" alt="img" align="right" width="400px">

# Book Highlights to Website with Semantic Search

📚 Do you love reading books and want to make the most of your highlights? Look no further! Welcome to the world of transforming your book highlights into an interactive, searchable vector space on your own website. This project was inspired by the desire to create a cost-effective, serverless, and automated solution for managing and exploring book highlights.

## Highlights of the Project

- 🚀 **Serverless & Automated:** This entire system is designed to work without the need for dedicated servers. It's fully automated, ensuring that every time you update your Google Sheet with highlights, your website reflects those changes within minutes.

- 💰 **No Cost Infrastructure:** Best of all, the infrastructure to make this magic happen comes at zero cost. Say goodbye to monthly hosting fees!

- 💌 **Daily Highlights in Your Inbox:** As a bonus, you'll receive three random highlights from your collection in your inbox every day. It's like having a daily dose of literary inspiration.

## See it in Action
- 🌐 **Live Website:** Check out the final result at [books.alessandroferrari.live](https://books.alessandroferrari.live) to experience your book highlights like never before.

- 🪄 **Interactive Visualization:** Explore a live representation of your highlights in a dynamic vector space. Simply hover your mouse over the dots to discover your insights.

## How it Works

### Step 1: Getting the Data
To get started, your book highlights should be organized in a Google Sheet in a specific format. The important information to include is the highlight text and the ISBN. Don't worry about any other details; they're just unnecessary baggage. 

### Step 2: Formatting the Data
The next step is to format your data in a way that can be understood by Jekyll, a static site generator. A Python script extracts your data from the Google Sheet and generates Markdown files. These files include author names, book titles, cover images, and publishing dates, all fetched from the Google Books API.

### Step 3: Generating Embeddings
To add a layer of sophistication, embeddings are generated from your highlights using sentence-transformers. This powerful step allows for features like clustering and semantic search. A second Python script takes care of this task, transforming your highlights into a 384-dimensional dense vector space.

### Step 4: Deploying the Website
With your data and embeddings ready, it's time to deploy your website. Using a static site generator like Jekyll, your website is generated. Now, all your book highlights are live and accessible to you and your audience.

### Step 5: Semantic Search
The heart of the system lies in semantic search. A serverless Netlify function enables you to input queries and find similar highlights based on semantic similarity. It's like having your own personal literary search engine at your fingertips.

## Interact with Your Highlights
Not only can you explore your highlights on your website, but you can also interactively visualize them in a dynamic vector space. This feature lets you see your highlights in a new light, clustering them by books and topics.

## Email Quotes to Your Inbox
One more cherry on top! You can set up a Google AppScript trigger to send you three random highlights from your collection every day. It's an excellent way to revisit your favorite quotes and keep them fresh in your mind.

## Get Started
Ready to embark on this literary adventure? Head over to the [GitHub repository](https://github.com/your-repo-url) to get started with the code and detailed instructions.

## Conclusion
This project not only enhances your reading experience but also showcases the practical application of machine learning in personal projects. While it's publicly accessible, you'll probably be the one benefiting from it the most, as you can always look back at your own highlights.

Start exploring your book highlights like never before at [books.alessandroferrari.live](https://books.alessandroferrari.live)!

Happy reading! 📚
