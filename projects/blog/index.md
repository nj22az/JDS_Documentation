---
layout: default
title: Home
---

# Engineering Notes

<ul class="post-list">
{% for post in site.posts %}
  <li>
    <span class="post-date">{{ post.date | date: "%B %-d, %Y" }}</span>
    <h2 class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 40 }}</p>
  </li>
{% endfor %}
</ul>
