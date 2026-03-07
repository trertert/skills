---
name: telegraph-backlinks
description: Create SEO backlink articles on Telegraph (telegra.ph, DA 93, dofollow, indexable). No auth required — instant publish via API. Use when asked to build Telegraph backlinks, create telegra.ph articles with links, or scale quick backlink pages. Supports single creation, batch mode, account management, and token reuse.
---

# Telegraph Backlinks

Publish articles on telegra.ph (DA 93, dofollow links, Google-indexable) with contextual backlinks. Zero friction — one API call, instantly live.

## Quick Start

```bash
# Create article with inline content
python3 scripts/telegraph-backlink.py create \
  --target "https://www.example.com" \
  --title "Article Title" \
  --content sections.json \
  --anchors "anchor text 1" "anchor text 2" \
  --author "BrandName"

# Batch create
python3 scripts/telegraph-backlink.py batch --file batch.json --output results.json

# List all pages across saved accounts
python3 scripts/telegraph-backlink.py list

# Create reusable account
python3 scripts/telegraph-backlink.py account --name "BrandName" --url "https://www.example.com"
```

All paths relative to this skill directory.

## Content JSON Format

Content is an array of section objects:

```json
[
  {"tag": "h3", "text": "Section Heading"},
  {"tag": "p", "text": "Paragraph with {backlink} placed naturally in the text."},
  {"tag": "p", "text": "Regular paragraph without a link."},
  {"tag": "ul", "items": [
    {"term": "Bold term", "desc": "Description"},
    "Simple list item"
  ]},
  {"tag": "blockquote", "text": "A quoted passage."}
]
```

- `{backlink}` placeholders get replaced with anchor links to the target URL
- Each `{backlink}` consumes one anchor from `--anchors` in order
- Supported tags: `h3`, `h4`, `p`, `ul`, `blockquote`

## Batch JSON Format

```json
[
  {
    "target": "https://www.example.com",
    "title": "Article Title",
    "author": "BrandName",
    "anchors": ["anchor 1", "anchor 2"],
    "sections": [
      {"tag": "h3", "text": "Heading"},
      {"tag": "p", "text": "Text with {backlink} here."}
    ]
  }
]
```

## How It Works

1. **Account creation** — `createAccount` API returns access token (saved to `~/.config/openclaw/telegraph-tokens.json` for reuse)
2. **Page creation** — `createPage` API publishes instantly, returns live URL
3. **Author URL** — set to target URL for an extra link signal in the byline

## Token Management

- Tokens auto-save to `~/.config/openclaw/telegraph-tokens.json`
- Reused automatically when `--author` matches a saved account name
- One account can create unlimited pages
- Use different author names per campaign/brand for separation

## Content Guidelines

- **800+ words** for SEO value — thin content risks deindexing
- **2 backlinks per article** with varied anchor text
- **Relevant content** — Telegraph pages rank well when topically coherent
- **No images** via API (text/HTML only) — keep content text-rich
- Telegraph supports: `h3`, `h4`, `p`, `a`, `ul`, `ol`, `li`, `b`, `i`, `blockquote`, `figure`, `img`, `pre`, `code`, `aside`, `br`, `hr`

## Key Details

- **DA:** ~93 (high authority)
- **Links:** Dofollow
- **Indexing:** Google crawls telegra.ph regularly
- **Rate limits:** None documented, but add 1s delay between batch posts
- **No account needed:** Token created on the fly
- **Editing:** Pages can be edited later with the same token via `editPage` API
- **Author byline:** Links to author_url — set this to target URL for bonus link
