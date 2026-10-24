"""Build all eight static pages using only Python's standard library.

Edit templates/pages/*.html for page content, templates/base.html for the shared
layout, and data/*.json for publications, media, and repositories. Run this script
from any directory. Generated root HTML files work on GitHub Pages or directly.
"""
import json
import re
from collections import Counter
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    "index": ("Home", "Sonith L. S., PhD candidate at the Indian Institute of Astrophysics, Bengaluru, awaiting thesis defence and studying classical symbiotic outbursts and interacting binaries."),
    "bio": ("Bio", "Sonith L. S.: biography, education, astronomy outreach, and scientific community service."),
    "research": ("Research", "Research on symbiotic stars, interacting binaries, stellar outbursts, and multi-wavelength observations."),
    "publications": ("Publications", "Search Sonith L. S.’s journal articles, manuscripts, conference contributions, and Astronomer’s Telegrams."),
    "media": ("Media & Outreach", "Research coverage and astronomy outreach by Sonith L. S.: TCP J1822, YY Herculis, and public discussions in Malayalam."),
    "repositories": ("Repositories", "Astronomy research software and Python resources by Sonith L. S."),
    "cv": ("CV", "Sonith L. S.’s curriculum vitae: education, observing experience, technical expertise, and presentations."),
    "contact": ("Contact", "Contact Sonith L. S. at the Indian Institute of Astrophysics for research collaborations and outreach."),
}


def text(value):
    return escape(str(value), quote=True)


def link(value):
    if value and (urlparse(value).scheme != "https" or not urlparse(value).netloc):
        raise ValueError(f"Expected an absolute HTTPS URL: {value}")
    return text(value)


def publication_html(item):
    if item["type"] not in {"journal", "progress", "conference", "telegram"}:
        raise ValueError(f"Unknown publication type: {item['type']}")
    year = int(item["year"])
    title = text(item["title"])
    url = link(item.get("url", ""))
    heading = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>' if url else title
    authors = text(item["authors"]).replace("Sonith, L. S.", "<strong>Sonith, L. S.</strong>")
    badge = "publication-badge progress" if item["type"] == "progress" else "publication-badge"
    paper_link = f'<a class="paper-link" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Read {title}">Read paper <span aria-hidden="true">↗</span></a>' if url else ""
    return f'''<article class="publication" data-year="{year}" data-type="{item['type']}" data-keywords="{text(item.get('keywords', ''))}">
  <span class="publication-year">{year}</span>
  <div class="publication-body"><h2>{heading}</h2><p class="publication-authors">{authors}</p><p class="publication-venue">{text(item['venue'])}</p><div class="publication-meta"><span class="{badge}">{text(item['status'])}</span>{paper_link}</div></div>
</article>'''


def media_html(item):
    published = date.fromisoformat(item["date"]) if item.get("date") else None
    date_html = f'<time datetime="{published.isoformat()}">{text(item.get("date_label", published.strftime("%d %b %Y")))}</time>' if published else '<span></span>'
    url = link(item.get("url", ""))
    story_link = f'<a class="inline-link" href="{url}" target="_blank" rel="noopener noreferrer">{text(item.get("link_label", "Read more"))} <span aria-hidden="true">↗</span></a>' if url else ""
    thumbnail = item.get("thumbnail", "")
    preview = ""
    if thumbnail:
        # Keep image paths inside this checkout; they are served as local assets.
        asset = (ROOT / thumbnail).resolve()
        if ROOT not in asset.parents or not asset.is_file():
            raise ValueError(f"Invalid media thumbnail: {thumbnail}")
        preview = f'<a class="video-preview" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Watch {text(item["title"])}"><span class="media-image-frame"><img src="{text(thumbnail)}" alt="" width="260" height="200" loading="lazy"></span><span>Watch on YouTube</span></a>'
    figure = item.get("figure", "")
    if figure:
        asset = (ROOT / figure).resolve()
        if ROOT not in asset.parents or not asset.is_file():
            raise ValueError(f"Invalid media figure: {figure}")
        preview = f'<figure class="research-figure"><a class="media-image-frame" href="{text(figure)}" target="_blank" rel="noopener noreferrer"><img src="{text(figure)}" alt="{text(item["figure_alt"])}" loading="lazy"></a><figcaption>{text(item["figure_caption"])}</figcaption></figure>'
    return f'''<article class="media-card">
  {date_html}
  <div><div class="media-meta"><span>{text(item['category'])}</span><span>{text(item['source'])}</span></div><h3>{text(item['title'])}</h3><div class="media-detail">{preview}<div><p>{text(item['summary'])}</p>{story_link}</div></div></div>
</article>'''


def repository_html(item):
    return f'''<article class="repository-card">
  <div class="repo-heading"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M5 3h14v18H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 0v14h14M7 21v-4"/></svg><h3><a href="{link(item['url'])}" target="_blank" rel="noopener noreferrer">{text(item['name'])}</a></h3></div>
  <p>{text(item['description'])}</p><div class="repo-meta"><span class="language-dot {text(item['language_class'])}" aria-hidden="true"></span><span>{text(item['language'])}</span><span>{text(item['category'])}</span></div>
</article>'''


def render(template, values):
    def substitute(match):
        key = match.group(1)
        if key not in values:
            raise ValueError(f"Missing template value: {key}")
        return values[key]
    return re.sub(r"\{\{([A-Z_]+)\}\}", substitute, template)


def main():
    def load(name):
        return json.loads((ROOT / f"data/{name}.json").read_text(encoding="utf-8"))
    publications = sorted(load("publications"), key=lambda item: int(item["year"]), reverse=True)
    media = sorted(load("media"), key=lambda item: date.fromisoformat(item["date"]) if item.get("date") else date.min, reverse=True)
    for item in media:
        if item["section"] not in {"research", "outreach"}:
            raise ValueError(f"Unknown media section: {item['section']}")
    repositories = load("repositories")
    counts = Counter(item["type"] for item in publications)
    years = sorted({int(item["year"]) for item in publications}, reverse=True)
    shared = {
        "PUBLICATIONS": "\n".join(map(publication_html, publications)),
        "MEDIA_ITEMS": "\n".join(media_html(item) for item in sorted(media, key=lambda item: item.get("display_priority", 999))),
        "RESEARCH_MEDIA": "\n".join(media_html(item) for item in media if item["section"] == "research"),
        "OUTREACH_MEDIA": "\n".join(media_html(item) for item in media if item["section"] == "outreach"),
        "REPOSITORIES": "\n".join(map(repository_html, repositories)),
        "YEARS": "\n".join(f'<option value="{year}">{year}</option>' for year in years),
        "JOURNAL_COUNT": str(counts["journal"]),
        "PROGRESS_COUNT": str(counts["progress"]),
    }
    base = (ROOT / "templates/base.html").read_text(encoding="utf-8")
    outputs = {}
    for slug, (label, description) in PAGES.items():
        nav = []
        for other, (nav_label, _) in PAGES.items():
            if other == "index":
                continue
            active = ' aria-current="page"' if other == slug else ""
            nav.append(f'<a href="{other}.html"{active}>{text(nav_label)}</a>')
        content = render((ROOT / f"templates/pages/{slug}.html").read_text(encoding="utf-8"), shared)
        outputs[slug] = render(base, {
            "TITLE": "Sonith L. S. | Observational Astrophysicist" if slug == "index" else text(f"{label} | Sonith L. S."),
            "DESCRIPTION": text(description),
            "CANONICAL": "" if slug == "index" else f"{slug}.html",
            "BODY_CLASS": "home-page" if slug == "index" else "inner-page",
            "MAIN_CLASS": "home-main" if slug == "index" else "page-content",
            "NAVIGATION": "\n        ".join(nav),
            "CONTENT": content,
        })
    for slug, html in outputs.items():
        (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")
    # Preserve the old news URL, including for visitors with JavaScript disabled.
    (ROOT / "news.html").write_text('''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Media &amp; Outreach | Sonith L. S.</title><meta http-equiv="refresh" content="0; url=media.html"><link rel="canonical" href="https://sonithls.github.io/media.html"></head><body><p>This page has moved to <a href="media.html">Media &amp; Outreach</a>.</p></body></html>
''', encoding="utf-8")
    print(f"Built {len(outputs)} pages and a news redirect: {len(publications)} publications, {len(media)} media items, {len(repositories)} repositories.")


if __name__ == "__main__":
    main()
