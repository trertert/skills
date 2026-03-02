---
name: google-patents
description: >
  Search Google Patents database for patent research, infringement risk checks, and competitive IP analysis.
  Use when user mentions: 专利, patent, 侵权, infringement, 知识产权, IP, 外观设计, design patent,
  专利检索, patent search, 专利风险, patent risk, 专利分析, patent analysis, 专利布局, patent portfolio,
  有没有专利, 会不会侵权, 能不能卖, FTO, freedom to operate, 规避设计, 专利壁垒, 技术壁垒,
  权利要求, claims, 专利详情, 发明人, inventor, 受让人, assignee, 专利号, patent number,
  说明书, description, 技术领域, 背景技术, 发明内容, 具体实施方式
---

# Google Patents

Search and retrieve patent data via SerpApi. Requires SERPAPI_API_KEY env var (free: 100/month, get at serpapi.com).

## 4 Commands

```bash
# Search patents
bash scripts/patents.sh search "keywords" [options]

# Get patent detail (basic info + claims)
bash scripts/patents.sh detail "US11734097B1"

# Get description full text only
bash scripts/patents.sh fulltext "US11734097B1"

# Get EVERYTHING in one call (detail + claims + full description)
bash scripts/patents.sh full "US11734097B1"
```

Patent ID: use short form `US11734097B1` or full `patent/US11734097B1/en`.

## Search Options

```
--country US,CN,JP,WO,EP,KR,DE    Filter by country
--status GRANT|APPLICATION          Granted or pending
--type PATENT|DESIGN                Invention or design patent
--assignee "Company"                Filter by company
--inventor "Name"                   Filter by inventor
--after publication:20230101        Min date (priority|filing|publication)
--before publication:20251231       Max date
--sort relevance|new|old            Sort order
--num 10-100                        Results per page
--page N                            Pagination
--language ENGLISH|CHINESE|JAPANESE Language filter
--litigation YES|NO                 Litigation history
--scholar                           Include Google Scholar
--clustered                         Group by CPC class
```

## Search Query Syntax

```bash
# Boolean
bash scripts/patents.sh search "(massage) AND (glove OR mitt)"
# Multi-term + CPC class (semicolon separator)
bash scripts/patents.sh search "(pet grooming);(A01K13)"
```

## What Each Command Returns

**search**: organic_results[] with patent_id, title, snippet, assignee, inventor, dates, pdf, country_status

**detail**: title, abstract, claims[], inventors[], assignees[], classifications[], legal_events[], patent_citations, cited_by, similar_documents[], images[], pdf, family_id, worldwide_applications

**fulltext**: patent_id, description (full text with headings: FIELD OF INVENTION, BACKGROUND, SUMMARY, DETAILED DESCRIPTION, etc.)

**full**: Everything from detail + description_full (all-in-one)

## E-commerce Scenarios

### Infringement risk (pre-listing must-do)
```bash
bash scripts/patents.sh search "product name" --type DESIGN --country US --status GRANT
```

### Competitor patent portfolio
```bash
bash scripts/patents.sh search "category" --assignee "Company" --num 50
```

### Category patent density
```bash
bash scripts/patents.sh search "category" --status GRANT --country US --num 100
```

### Expired patents (free to use)
```bash
bash scripts/patents.sh search "tech" --before "filing:20040101" --country US
```

### Latest trends
```bash
bash scripts/patents.sh search "tech" --sort new --after "publication:20240101"
```

### Litigation-prone patents
```bash
bash scripts/patents.sh search "product" --litigation YES --country US
```

### Full patent analysis (read claims to assess real infringement risk)
```bash
bash scripts/patents.sh full "USD975937S1"
```

## Features
- Auto-retry (3x) on 429/5xx errors with exponential backoff
- Auto-normalize patent ID (short or full format)
- Description full text extraction (HTML to clean text)
- All-in-one command for complete patent data
- Chinese and English supported
- All Google Patents countries supported

## Notes
- English keywords work best; Chinese supported but less coverage
- Free tier: 100 searches/month; cached hits free
- Design patents (--type DESIGN) = #1 infringement risk for e-commerce
- `full` command uses 1 API call (detail) + 1 HTTP fetch (description)
