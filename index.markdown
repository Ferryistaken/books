---
layout: default
---

# My Book Highlights

---

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

[How I made this](https://alessandroferrari.live/book-highlights).
<div style="text-align: center; margin: 0; overflow: hidden;">
<iframe src="/square-plot.html" width="450px" height="450px" style="border:none; max-width: 90vw; max-height: 90vh; margin: 0; padding: 0;"></iframe>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px;">
  {% assign sorted_books = site.books | sort: 'first-author-last-name' %}
  {% for book in sorted_books %}
    <div class="book-container">
      <a href="{{ book.url | relative_url }}"><img class="book-image" src="{{ book.coverImage }}" alt="{{ book.title }}"></a>
      <h2 class="book-title"><a href="{{ book.url | relative_url }}">{{ book.title }}</a></h2>
      <p class="book-author">{{ book.authors | join: ', ' }}</p>
    </div>
  {% endfor %}
</div>
