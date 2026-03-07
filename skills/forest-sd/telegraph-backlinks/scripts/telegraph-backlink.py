#!/usr/bin/env python3
"""
Telegraph Backlink Generator
Creates articles on telegra.ph with contextual backlinks to target URLs.
No authentication required — just API calls.

Usage:
  # Create account + post article
  python3 telegraph-backlink.py create \
    --target "https://www.example.com" \
    --title "Article Title Here" \
    --content content.json \
    --anchors "anchor text 1" "anchor text 2" \
    --author "Brand Name"

  # Post with existing token
  python3 telegraph-backlink.py create \
    --token "abc123..." \
    --target "https://www.example.com" \
    --title "Article Title" \
    --content content.json \
    --anchors "anchor 1" "anchor 2"

  # Batch from JSON
  python3 telegraph-backlink.py batch --file batch.json --output results.json

  # List pages for a token
  python3 telegraph-backlink.py list --token "abc123..."

  # Create account only
  python3 telegraph-backlink.py account --name "Brand Name" --url "https://www.example.com"
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
import time

API_BASE = "https://api.telegra.ph"
TOKENS_FILE = os.path.expanduser("~/.config/openclaw/telegraph-tokens.json")


def api_call(method, params):
    """Make a Telegraph API call."""
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"{API_BASE}/{method}", data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if not result.get("ok"):
        print(f"❌ API error: {result}")
        return None
    return result["result"]


def load_tokens():
    """Load saved tokens."""
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE) as f:
            return json.load(f)
    return {}


def save_token(name, token, author_url=""):
    """Save a token for reuse."""
    tokens = load_tokens()
    tokens[name] = {"token": token, "author_url": author_url}
    os.makedirs(os.path.dirname(TOKENS_FILE), exist_ok=True)
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)


def create_account(short_name, author_name=None, author_url=""):
    """Create a Telegraph account and return access token."""
    params = {"short_name": short_name[:32]}
    if author_name:
        params["author_name"] = author_name[:128]
    if author_url:
        params["author_url"] = author_url
    result = api_call("createAccount", params)
    if result:
        save_token(short_name, result["access_token"], author_url)
        return result["access_token"]
    return None


def build_content(sections, target_url, anchors):
    """Build Telegraph content nodes from sections with backlink insertion.
    
    Sections format:
    [
        {
            "tag": "h3" | "p" | "ul",
            "text": "paragraph text with {backlink} placeholder",
            "items": ["list item 1", "list item 2"]  # for ul only
        }
    ]
    """
    nodes = []
    anchor_idx = 0

    for section in sections:
        tag = section.get("tag", "p")

        if tag in ("h3", "h4"):
            nodes.append({"tag": tag, "children": [section["text"]]})

        elif tag == "p":
            text = section["text"]
            if "{backlink}" in text and anchor_idx < len(anchors):
                # Split on {backlink} and insert link node
                parts = text.split("{backlink}", 1)
                children = []
                if parts[0]:
                    children.append(parts[0])
                children.append({
                    "tag": "a",
                    "attrs": {"href": target_url},
                    "children": [anchors[anchor_idx]]
                })
                if parts[1]:
                    children.append(parts[1])
                anchor_idx += 1
                nodes.append({"tag": "p", "children": children})
            else:
                nodes.append({"tag": "p", "children": [text]})

        elif tag == "ul":
            items = []
            for item in section.get("items", []):
                if isinstance(item, dict):
                    items.append({"tag": "li", "children": [
                        {"tag": "b", "children": [item["term"]]},
                        f" — {item['desc']}"
                    ]})
                else:
                    items.append({"tag": "li", "children": [item]})
            nodes.append({"tag": "ul", "children": items})

        elif tag == "blockquote":
            nodes.append({"tag": "blockquote", "children": [section["text"]]})

    return nodes


def create_page(token, title, content_nodes, author_name=None, author_url=""):
    """Create a Telegraph page."""
    params = {
        "access_token": token,
        "title": title[:256],
        "content": json.dumps(content_nodes),
        "return_content": "false",
    }
    if author_name:
        params["author_name"] = author_name[:128]
    if author_url:
        params["author_url"] = author_url

    result = api_call("createPage", params)
    if result:
        return {
            "url": result["url"],
            "path": result["path"],
            "title": result["title"],
            "views": result.get("views", 0),
        }
    return None


def cmd_create(args):
    # Get or create token
    token = args.token
    if not token:
        tokens = load_tokens()
        if args.author and args.author in tokens:
            token = tokens[args.author]["token"]
            print(f"♻️  Reusing token for '{args.author}'")
        else:
            name = args.author or "Backlinks"
            print(f"🔑 Creating account: {name}")
            token = create_account(name, name, args.target)
            if not token:
                print("❌ Failed to create account")
                return

    # Load content
    if args.content:
        with open(args.content) as f:
            sections = json.load(f)
    elif args.raw_content:
        sections = json.loads(args.raw_content)
    else:
        print("❌ Need --content (file) or --raw-content (JSON string)")
        return

    # Build nodes
    nodes = build_content(sections, args.target, args.anchors)

    # Create page
    print(f"📝 Publishing: {args.title}")
    result = create_page(token, args.title, nodes, args.author, args.target)
    if result:
        print(f"✅ Live: {result['url']}")
        print(json.dumps(result, indent=2))
    else:
        print("❌ Failed to create page")


def cmd_batch(args):
    with open(args.file) as f:
        batch = json.load(f)

    results = []
    for i, item in enumerate(batch):
        # Get or create token per author
        author = item.get("author", "Backlinks")
        target = item["target"]
        tokens = load_tokens()

        if author in tokens:
            token = tokens[author]["token"]
        else:
            token = create_account(author, author, target)
            if not token:
                print(f"❌ Failed to create account for {author}")
                continue

        nodes = build_content(item["sections"], target, item["anchors"])
        result = create_page(token, item["title"], nodes, author, target)

        if result:
            result["target"] = target
            result["anchors"] = item["anchors"]
            results.append(result)
            print(f"✅ [{i+1}/{len(batch)}] {result['url']}")
        else:
            print(f"❌ [{i+1}/{len(batch)}] Failed: {item['title']}")

        time.sleep(1)  # Rate limit courtesy

    print(f"\n{'='*60}")
    print(f"✅ Published {len(results)}/{len(batch)} pages")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")

    return results


def cmd_list(args):
    token = args.token
    if not token:
        tokens = load_tokens()
        if not tokens:
            print("No saved tokens. Use --token or create an account first.")
            return
        # List all accounts
        for name, data in tokens.items():
            print(f"\n📋 Account: {name}")
            result = api_call("getPageList", {
                "access_token": data["token"],
                "limit": 50,
            })
            if result:
                print(f"   Total pages: {result['total_count']}")
                for page in result.get("pages", []):
                    print(f"   🔗 {page['url']} ({page.get('views', 0)} views)")
        return

    result = api_call("getPageList", {"access_token": token, "limit": 50})
    if result:
        print(f"Total pages: {result['total_count']}")
        for page in result.get("pages", []):
            print(f"  🔗 {page['url']} ({page.get('views', 0)} views)")


def cmd_account(args):
    token = create_account(args.name, args.name, args.url or "")
    if token:
        print(f"✅ Account created: {args.name}")
        print(f"   Token: {token}")
        print(f"   Saved to: {TOKENS_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Telegraph Backlink Generator")
    sub = parser.add_subparsers(dest="command")

    # create
    p_create = sub.add_parser("create", help="Create a single Telegraph article")
    p_create.add_argument("--target", required=True, help="Target URL for backlinks")
    p_create.add_argument("--title", required=True, help="Article title")
    p_create.add_argument("--content", help="Path to content JSON file")
    p_create.add_argument("--raw-content", help="Content JSON as string")
    p_create.add_argument("--anchors", nargs="+", required=True, help="Anchor texts")
    p_create.add_argument("--author", help="Author name (reuses saved token if exists)")
    p_create.add_argument("--token", help="Telegraph access token (optional)")

    # batch
    p_batch = sub.add_parser("batch", help="Batch create from JSON")
    p_batch.add_argument("--file", required=True, help="Batch JSON file")
    p_batch.add_argument("--output", help="Save results to file")

    # list
    p_list = sub.add_parser("list", help="List pages")
    p_list.add_argument("--token", help="Access token (lists all saved if omitted)")

    # account
    p_acct = sub.add_parser("account", help="Create account only")
    p_acct.add_argument("--name", required=True, help="Short name")
    p_acct.add_argument("--url", help="Author URL")

    args = parser.parse_args()

    if args.command == "create":
        cmd_create(args)
    elif args.command == "batch":
        cmd_batch(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "account":
        cmd_account(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
