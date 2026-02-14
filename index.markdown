---
layout: books-home
---

<h1 style="font-size: clamp(4rem, 10vw, 10rem); font-weight: 400; text-align: left; letter-spacing: -0.03em; line-height: 1.05; font-family: 'Instrument Serif', Georgia, serif;">My <em style="font-style: italic;">Book</em> Highlights</h1>

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

{% assign count = site.books | size %}

{% assign total_highlights = 0 %}
{% assign total_pages = 0 %}
{% for book in site.books %}
  {% assign highlights_count = book.highlights | size %}
  {% assign total_highlights = total_highlights | plus: highlights_count %}
  {% assign total_pages = total_pages | plus: book.page_number %}
{% endfor %}

{% assign start_date = '2004-05-12' | date: '%s' %}
{% assign today = 'now' | date: '%s' %}
{% assign secondsSince = today | minus: start_date %}
{% assign daysSince = secondsSince | divided_by: 86400 %}

{% if daysSince > 0 %}
  {% assign pages_per_day_raw = total_pages | times: 1.0 | divided_by: daysSince %}
  {% assign pages_per_day = pages_per_day_raw | times: 100.0 | round: 0 | divided_by: 100.0 %}
{% else %}
  {% assign pages_per_day = 0 %}
{% endif %}

[How I made this](https://alessandroferrari.live/book-highlights) \| 📖 Books: {{count}} \| 💡 Total Highlights: {{total_highlights}} \| 📚 Pages per Day (lifetime): {{pages_per_day}}


<div style="text-align: center; margin: 0; overflow: hidden;">
<iframe src="/square-plot.html" width="450px" height="450px" style="border:none; max-width: 90vw; max-height: 90vh; margin: 0; padding: 0; overflow: hidden;" scrolling="no"></iframe>
</div>

<div class="book-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px;">
  {% assign sorted_books = site.books | sort: 'first-author-last-name' %}
  {% for book in sorted_books %}
    <a href="{{ book.url | relative_url }}" style="text-decoration: none; color: inherit;">
      <div class="book-container">
        {% include lazyload.html image_src=book.coverImage image_alt=book.title image_title=book.title %}
        <h2 class="book-title">{{ book.title }}</h2>
        <p class="book-author">{{ book.authors | join: ', ' }}</p>
      </div>
    </a>
  {% endfor %}
</div>

<div style="text-align: center; margin-top: 20px;">
    <a href="/other" class="other-quotes-link">Other Quotes</a>
</div>
