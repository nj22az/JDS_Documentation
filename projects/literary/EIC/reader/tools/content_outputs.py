"""Write the generated reader, SEO, asset, and omnibus outputs."""

import html
import json
import os
import re
import shutil

from content_config import (
    APP,
    COMPILED_MARKDOWN,
    FALLBACK_EXCERPT_MAX_WORDS,
    HTML_ASSETS,
    INDEX_HTML,
    MANUSCRIPT,
    NARRATIVE_ROLES,
    OUT_OMNIBUS_CONFIG,
    OUT_PUBLIC,
    PUBLIC_ASSET_SUBDIRECTORIES,
)
from content_source import book_pages, parse_frontmatter


def inject_between(text, start, end, payload):
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    updated, replacements = pattern.subn(start + payload + end, text, count=1)
    if replacements != 1:
        raise SystemExit(f"index.html is missing marker pair: {start} / {end}")
    return updated


def fallback_excerpt(pages, max_words=FALLBACK_EXCERPT_MAX_WORDS):
    """Supply enough real prose for no-JS readers and reliable language detection."""
    excerpt = []
    words = 0
    for page_id, label in (("00a-foreword", "From the foreword"),
                           ("01-1603-the-boy-who-signed", "From Chapter One")):
        page = next((candidate for candidate in pages if candidate["id"] == page_id), None)
        if not page:
            continue
        body = re.sub(r"<figure.*?</figure>", "", page["body"], flags=re.S)
        paragraphs = re.findall(r"<p>(.*?)</p>", body, flags=re.S)
        section = [f"<h2>{label}</h2>"]
        for paragraph in paragraphs:
            if words >= max_words:
                break
            section.append(f"<p>{paragraph}</p>")
            plain = re.sub(r"<[^>]+>", "", paragraph)
            words += len(plain.split())
        if len(section) > 1:
            excerpt.extend(section)
    return "\n        ".join(excerpt)


def build_seo(manifest, pages):
    publication = manifest["publication"]
    site_url = publication["site_url"]
    cover_url = site_url + "assets/generated/front-row-seat-cover.png"
    jsonld_books = []
    fallback_sections = []

    for position, book in enumerate(manifest["books"], start=1):
        jsonld_books.append({
            "@type": "Book",
            "position": position,
            "name": book["title"],
            "temporalCoverage": book["years"].replace("–", "/"),
            "url": site_url + "#/read/" + book["landing_id"],
        })
        narrative = [page for page in book_pages(book, pages) if page["role"] in NARRATIVE_ROLES]
        items = "\n".join(
            f'              <li><a href="#/read/{page["id"]}">{html.escape(page["title"])}'
            + (f' <span>({html.escape(page["year"])})</span>' if page["year"] else "")
            + "</a></li>"
            for page in narrative
        )
        fallback_sections.append(
            "          <section>\n"
            f'            <h2>Book {book["word"]} &mdash; {html.escape(book["title"])} '
            f'<small>({html.escape(book["years"])})</small></h2>\n'
            "            <ol>\n"
            f"{items}\n"
            "            </ol>\n"
            "          </section>"
        )

    jsonld = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": publication["title"],
        "alternativeHeadline": publication["subtitle"],
        "bookEdition": "Illustrated omnibus edition; Book One expanded novel",
        "author": {"@type": "Person", "name": "Nils Johansson"},
        "inLanguage": "en",
        "bookFormat": "https://schema.org/EBook",
        "url": site_url,
        "image": cover_url,
        "description": publication["description"],
        "hasPart": jsonld_books,
    }
    jsonld_html = (
        "\n    <script type=\"application/ld+json\">"
        + json.dumps(jsonld, ensure_ascii=False, separators=(",", ":"))
        + "</script>\n    "
    )
    fallback = f"""
      <main lang="en" style="max-width:40rem;margin:0 auto;padding:2rem 1.25rem;font-family:Georgia,serif;line-height:1.6;color:#1d1d1f">
        <h1>{html.escape(publication["title"])}</h1>
        <p><em>{html.escape(publication["subtitle"])}</em></p>
        <p>Six books by Nils Johansson follow five centuries of the East India Company from one riverside tavern on the Thames.</p>
        <p>Book One, <em>The Venture</em>, is now the complete 100,000-word historical novel. Books Two through Six remain compact editions.</p>
        <p><a href="#/">Open the interactive reader &rarr;</a></p>
        <nav aria-label="Six books and their chapters">
{os.linesep.join(fallback_sections)}
        </nav>
        {fallback_excerpt(pages)}
        <p>If you are reading this, the interactive reader is still loading &mdash; it will replace this page shortly.</p>
      </main>
      """

    index_source = INDEX_HTML.read_text(encoding="utf-8")
    index_source = inject_between(
        index_source, "<!-- seo:jsonld:start -->", "<!-- seo:jsonld:end -->", jsonld_html
    )
    index_source = inject_between(
        index_source, "<!-- seo:fallback:start -->", "<!-- seo:fallback:end -->", fallback
    )
    INDEX_HTML.write_text(index_source, encoding="utf-8")

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{site_url}</loc><changefreq>monthly</changefreq>'
        '<priority>1.0</priority></url>\n'
        '</urlset>\n'
    )
    (APP / "public").mkdir(parents=True, exist_ok=True)
    (APP / "public" / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    ordered_page_count = sum(len(book_pages(book, pages)) for book in manifest["books"])
    print(f"SEO: six-book schema and {ordered_page_count} ordered pages")


def write_omnibus_config(manifest, pages):
    books = []
    reader_book_ids = []
    for book in manifest["books"]:
        visible = book_pages(book, pages)
        narrative = [page for page in visible if page["role"] in NARRATIVE_ROLES]
        item = {
            "numeral": book["numeral"],
            "word": book["word"],
            "title": book["title"],
            "years": book["years"],
            "id": book["landing_id"],
            "words": sum(page["words"] for page in narrative),
        }
        if book.get("status"):
            item["status"] = book["status"]
        books.append(item)
        reader_book_ids.append([page["id"] for page in visible])

    chapter_words = {
        page["id"]: page["words"]
        for page in pages
        if not page["hidden"] and page["role"] in NARRATIVE_ROLES
    }
    taglines = {page["id"]: page["tagline"] for page in pages if page["tagline"]}
    config = {
        "books": books,
        "readerBookIds": reader_book_ids,
        "chapterWords": chapter_words,
        "chapterTaglines": taglines,
        "readingSpeed": manifest["publication"]["reading_speed"],
    }
    OUT_OMNIBUS_CONFIG.write_text(
        "window.FRONT_ROW_OMNIBUS = "
        + json.dumps(config, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )


def write_compiled_markdown(specs, source_by_id):
    ordered_sources = []
    for spec in specs:
        path = MANUSCRIPT / spec["path"]
        metadata, page_markdown = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        ordered_sources.append(page_markdown.strip())
        if metadata["id"] not in source_by_id:
            raise SystemExit(f"compiled export missing page id: {metadata['id']}")
    COMPILED_MARKDOWN.write_text("\n\n".join(ordered_sources) + "\n", encoding="utf-8")


def copy_public_assets():
    OUT_PUBLIC.mkdir(parents=True, exist_ok=True)
    for subdirectory in PUBLIC_ASSET_SUBDIRECTORIES:
        source = HTML_ASSETS / subdirectory
        if not source.is_dir():
            continue
        destination = OUT_PUBLIC / subdirectory
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination, ignore=shutil.ignore_patterns("._*", ".DS_Store"))
