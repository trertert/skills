---
name: "yanpan-finance"
description: "A-share financial data MCP Server - broker research reports, AI news analysis, and stock comprehensive analysis"
version: "1.2.0"
category: "finance"
tags: ["finance", "stock", "research-report", "news-analysis", "mcp", "A-share", "China"]
complexity: "beginner"
author: "Li-Evan"
---

# YanPan Finance MCP Server

Hosted MCP server providing A-share (China stock market) financial data for AI agents. Connect directly — no deployment needed.

## Tools

### `search_research_reports`
Search broker research reports by company name. Returns full-text reports including title, source, content, and date.
- **Input**: `company_name` (e.g. "比亚迪"), `limit` (default 10)
- **Coverage**: 5,000+ research reports, continuously updated

### `search_news_analysis`
Search AI-analyzed news by company name and date range. Returns original news, AI summary, sentiment analysis, investment recommendations, and importance score.
- **Input**: `company_name`, `start_date` (optional), `end_date` (optional), `limit` (default 10)
- **Coverage**: 19,000+ analyzed news items covering individual stocks and industries

### `get_stock_analysis`
Get the latest comprehensive analysis for a stock by its code. Returns technical analysis, fundamental analysis, news sentiment, investment debate, risk management, and final trading decision.
- **Input**: `stock_code` (e.g. "601900", "000001", "300750")
- **Coverage**: 3,000+ stocks, 12,000+ analysis reports

## Setup

1. Get your API key from the author (contact via ClawHub)

2. Set the environment variable:
```bash
export YANPAN_API_KEY="your-api-key-here"
```

3. Add to your `.mcp.json`:
```json
{
  "mcpServers": {
    "yanpan": {
      "type": "http",
      "url": "http://42.121.167.42:9800/mcp",
      "headers": {
        "Authorization": "Bearer ${YANPAN_API_KEY}"
      }
    }
  }
}
```

No installation, no Docker, no database — just connect and use.
