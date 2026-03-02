#!/bin/bash
# Google Patents v1.1 - search, detail, fulltext, full(all-in-one)
API_KEY="${SERPAPI_API_KEY:-640dcea4484043e8b12c389a19c0354bd6ac2e396b42ba46d76ef69006d805f2}"
BASE="https://serpapi.com/search.json"
MAX_RETRIES=3

urlencode() { python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1"; }

fetch_with_retry() {
  local url="$1" attempt=1 delay=2
  while [ $attempt -le $MAX_RETRIES ]; do
    local resp http_code body
    resp=$(curl -s -w "\n%{http_code}" "$url")
    http_code=$(echo "$resp" | tail -1)
    body=$(echo "$resp" | sed '$d')
    if [ "$http_code" = "200" ]; then echo "$body"; return 0; fi
    if [ "$http_code" = "429" ] || [ "$http_code" -ge 500 ] 2>/dev/null; then
      >&2 echo "[Retry $attempt/$MAX_RETRIES] HTTP $http_code, wait ${delay}s..."
      sleep $delay; delay=$((delay * 2)); attempt=$((attempt + 1))
    else echo "$body"; return 0; fi
  done
  echo "{\"error\":\"Failed after $MAX_RETRIES retries\"}"; return 1
}

normalize_id() {
  local pid="$1"
  [[ "$pid" != patent/* ]] && [[ "$pid" != scholar/* ]] && pid="patent/${pid}/en"
  echo "$pid"
}

html_to_text() {
  python3 -c "
import sys,re,html
raw=sys.stdin.read()
t=re.sub(r'<heading>','\n## ',raw)
t=re.sub(r'</heading>','\n',t)
t=re.sub(r'<[^>]+>',' ',t)
t=re.sub(r'\s+',' ',t)
print(html.unescape(t).strip())
"
}

action="${1:-help}"; shift

case "$action" in
search|s)
  query="$1"; shift
  [ -z "$query" ] && { echo '{"error":"Missing query"}'; exit 1; }
  params="engine=google_patents&q=$(urlencode "$query")&api_key=$API_KEY"
  while [ $# -gt 0 ]; do
    case "$1" in
      --num) params="$params&num=$2"; shift 2;; --page) params="$params&page=$2"; shift 2;;
      --country) params="$params&country=$2"; shift 2;; --status) params="$params&status=$2"; shift 2;;
      --type) params="$params&type=$2"; shift 2;; --sort) params="$params&sort=$2"; shift 2;;
      --language) params="$params&language=$2"; shift 2;; --litigation) params="$params&litigation=$2"; shift 2;;
      --inventor) params="$params&inventor=$(urlencode "$2")"; shift 2;;
      --assignee) params="$params&assignee=$(urlencode "$2")"; shift 2;;
      --after) params="$params&after=$2"; shift 2;; --before) params="$params&before=$2"; shift 2;;
      --scholar) params="$params&scholar=true"; shift;; --clustered) params="$params&clustered=true"; shift;;
      *) shift;;
    esac
  done
  fetch_with_retry "$BASE?$params";;

detail|d) fetch_with_retry "$BASE?engine=google_patents_details&patent_id=$(urlencode "$(normalize_id "$1")")&api_key=$API_KEY";;

fulltext|desc)
  detail_json=$(fetch_with_retry "$BASE?engine=google_patents_details&patent_id=$(urlencode "$(normalize_id "$1")")&api_key=$API_KEY")
  desc_link=$(echo "$detail_json" | python3 -c "import sys,json;print(json.loads(sys.stdin.read()).get('description_link',''))" 2>/dev/null)
  [ -z "$desc_link" ] && { echo '{"error":"No description_link"}'; exit 1; }
  desc_text=$(curl -s "$desc_link" | html_to_text)
  python3 -c "import sys,json;print(json.dumps({'patent_id':sys.argv[1],'description':sys.argv[2]},ensure_ascii=False))" "$(normalize_id "$1")" "$desc_text";;

full|all)
  pid=$(normalize_id "$1")
  detail_json=$(fetch_with_retry "$BASE?engine=google_patents_details&patent_id=$(urlencode "$pid")&api_key=$API_KEY")
  desc_link=$(echo "$detail_json" | python3 -c "import sys,json;print(json.loads(sys.stdin.read()).get('description_link',''))" 2>/dev/null)
  desc_text=""
  [ -n "$desc_link" ] && desc_text=$(curl -s "$desc_link" | html_to_text)
  echo "$detail_json" | python3 -c "
import sys,json
data=json.loads(sys.stdin.read())
data['description_full']=sys.argv[1]
for k in ['search_metadata','search_parameters']:data.pop(k,None)
print(json.dumps(data,ensure_ascii=False))
" "$desc_text";;

help|*) echo "patents.sh v1.1 - Google Patents Search"
  echo "  search \"query\" [opts]  Search patents"
  echo "  detail \"ID\"            Basic info + claims"
  echo "  fulltext \"ID\"          Description full text"
  echo "  full \"ID\"              All data (detail + description)"
  echo "Options: --country --status --type --assignee --inventor --after --before --sort --num --page --language --litigation --scholar --clustered";;
esac
