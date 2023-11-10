---
layout: default
---

# My Book Highlights

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px;">
  {% for book in site.books %}
    <div style="border: 1px solid #ddd; padding: 10px;">
      <img src="{{ book.coverImage }}" alt="{{ book.title }}" style="max-width: 100%;">
      <h2><a href="{{ book.url | relative_url }}">{{ book.title }}</a></h2>
      <p>{{ book.authors | join: ', ' }}</p>
    </div>
  {% endfor %}
</div>
