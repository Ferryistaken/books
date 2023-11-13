---
layout: default
---

# My Book Highlights

---

<br>

<style>
  /* Add CSS styling for the book containers */
  .book-container {
    border: none; /* Remove the bounding outline */
    display: flex;
    flex-direction: column;
    align-items: center; /* Center the contents horizontally */
  }

  .book-image {
    max-width: 100%;
  }

  .book-title {
    text-align: center; /* Center the title text */
    margin-top: 10px; /* Add some top margin for spacing */
  }

  .book-author {
    margin-top: auto; /* Push the author text to the bottom */
  }
</style>

<!--{% include search.html %}-->

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px;">
  {% for book in site.books %}
    <div class="book-container">
      <img class="book-image" src="{{ book.coverImage }}" alt="{{ book.title }}">
      <h2 class="book-title"><a href="{{ book.url | relative_url }}">{{ book.title }}</a></h2>
      <p class="book-author">{{ book.authors | join: ', ' }}</p>
    </div>
  {% endfor %}
</div>

