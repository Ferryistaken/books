---
title: Tags
permalink: /tags/
layout: page
excerpt: Sorted articles by tags.
---

{% for tag in site.tags %}
  {% capture name %}{{ tag | first }}{% endcapture %}
  
  <h4 class="book-header" id="{{ name | downcase | slugify }}">
    {{ name }}
  </h4>
  
  {% for book in site.tags[name] %}
    <article class="books">
      <span class="books-date">{{ book.date | date: "%b %d" }}</span>
      <header class="books-header">
        <h4 class="books-title">
          <a href="{{ book.url }}">{{ book.title | escape }}</a>
        </h4>
      </header>
      <p class="books-authors">
        Authors: {{ book.authors | join: ', ' }}
      </p>
    </article>
  {% endfor %}
{% endfor %}

