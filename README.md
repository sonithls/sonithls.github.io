# Sonith L. S. — academic website

## Pages

| Page | File | Content |
| --- | --- | --- |
| Home | `index.html` | Round GitHub portrait, introduction, social links, quick links |
| Bio | `bio.html` | Biography, education, outreach, community |
| Research | `research.html` | Research interests and observing experience |
| Publications | `publications.html` | 17 records with keyword search, year and type filters |
| Media & Outreach | `media.html` | Research coverage, public talks, and outreach |
| Repositories | `repositories.html` | Selected public GitHub projects |
| CV | `cv.html` | Academic CV summary and PDF download |
| Contact | `contact.html` | Email, affiliation, GitHub, ORCID |

Top navigation uses real page links, with an active-page indicator. Each page supports direct access, reload, browser back/forward, and GitHub Pages. Existing homepage section links such as `#publications` redirect to the corresponding new page when JavaScript is available.

## Preview

Open `index.html` directly, or run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit http://localhost:8000. No package installation is needed. All page content remains readable without JavaScript, including publication and media records. JavaScript adds publication search/filters and the collapsible mobile menu.

## Edit and rebuild

**Root HTML files are generated. Edit the templates or data, then rebuild.**

```sh
python3 scripts/build.py
```

- Page text and structure: `templates/pages/<page>.html`.
- Shared header, footer, and metadata layout: `templates/base.html`.
- Navigation labels and page descriptions: `PAGES` in `scripts/build.py`.
- Publications: `data/publications.json`.
- Media and outreach entries: `data/media.json`.
- Repository cards: `data/repositories.json`.
- Colors, typography, and responsive/print layouts: `styles.css`.
- Search and mobile navigation: `script.js`.
- Portrait: `assets/sonith.jpg`.
- Site background: `assets/telescope-background.jpg` (original JPEG, metadata stripped).
- CV PDF: `Sonith_Academic_CV.pdf` (linked from the homepage, bio, and CV page; update template links if renamed).

The builder uses only Python’s standard library. It renders all eight pages, escapes JSON content, validates external data URLs, and sorts publications/media by date. Commit changed sources **and the generated root HTML files** when publishing.

### Add media or outreach

Add an object to the array in `data/media.json`, then rebuild:

```json
{
  "date": "2026-10-05",
  "section": "research",
  "category": "Research highlight",
  "source": "Research notes",
  "title": "Your media headline",
  "summary": "A short description of the update.",
  "url": "",
  "link_label": "Read more"
}
```

Use dates in `YYYY-MM-DD` format, or an empty date for undated outreach. An optional `date_label` supplies a display label for date ranges. `url` can be empty for a text-only update, or an absolute HTTPS URL. Entries appear newest first, with optional `display_priority` values placing featured entries first (lower numbers first). Use `"section": "research"` for research coverage or `"section": "outreach"` for public talks and engagement. An optional `thumbnail` can refer to an existing local image.

### Update publications

Each publication has `year`, `title`, `authors`, `venue`, `type`, `status`, `keywords`, and `url`. Types are `journal`, `progress`, `conference`, or `telegram`. Use `progress` for manuscripts under review or in preparation. Leave `url` empty when no public record exists.

### Update repositories

Edit `data/repositories.json`. Each card has `name`, `description`, `language`, `language_class`, `category`, and an HTTPS `url`. `language_class` controls the small language-color dot in CSS. Cards do not rely on external statistics widgets or live API access.

## GitHub Pages

Publish the generated HTML files, `styles.css`, `script.js`, `assets/`, `.nojekyll`, and the PDF to the branch configured in **Settings → Pages**, using **Deploy from a branch → /(root)**. The source templates and JSON can stay in the same repository for future edits. No server or build pipeline is required on GitHub. The old `news.html` URL redirects to `media.html`; include it when publishing.

The existing Google verification file is preserved. Building locally does not commit, push, publish, or change repository settings.
