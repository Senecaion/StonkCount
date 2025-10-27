import os, re, json, time, datetime as dt
from collections import Counter
import requests
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env if present

BEARER = os.getenv("X_BEARER_TOKEN")
if not BEARER:
    raise SystemExit("❌ Missing X_BEARER_TOKEN. Put it in a .env file or your environment.")

ACCOUNT = "unusual_whales"
HEADERS = {"Authorization": f"Bearer {BEARER}"}

# Matches $TSLA, $AAPL, $BRK.B, $RDS-A, $SHOP.TO, etc.
CASHTAG_RE = re.compile(r"\$([A-Za-z]{1,5}(?:[.\-][A-Za-z0-9]{1,3})?)\b")

def iso_24h_window():
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    start = (now - dt.timedelta(hours=24))
    return start.isoformat().replace("+00:00","Z"), now.isoformat().replace("+00:00","Z")

def get_user_id(handle: str) -> str:
    url = f"https://api.twitter.com/2/users/by/username/{handle}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()["data"]["id"]

def fetch_tweets_24h(user_id: str, start_iso: str, end_iso: str):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": 100,
        "start_time": start_iso,
        "end_time": end_iso,
        "tweet.fields": "created_at,referenced_tweets",
        "exclude": "replies"  # include replies? remove this key
    }
    next_token = None
    while True:
        if next_token:
            params["pagination_token"] = next_token
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if r.status_code == 429:
            reset = int(r.headers.get("x-rate-limit-reset", "0"))
            sleep_for = max(5, reset - int(time.time()))
            time.sleep(min(sleep_for, 60))
            continue
        r.raise_for_status()
        data = r.json()
        for t in data.get("data", []):
            yield t
        next_token = (data.get("meta") or {}).get("next_token")
        if not next_token:
            break

def extract_cashtags(text: str):
    # unique per tweet (so "$TSLA $TSLA" counts once)
    return {m.group(1).upper() for m in CASHTAG_RE.finditer(text or "")}

def main():
    start_iso, end_iso = iso_24h_window()
    uid = get_user_id(ACCOUNT)

    counts = Counter()
    scanned = 0

    for tweet in fetch_tweets_24h(uid, start_iso, end_iso):
        scanned += 1
        for tag in extract_cashtags(tweet.get("text", "")):
            counts[tag] += 1

    result = {
        "account": f"@{ACCOUNT}",
        "window_start_utc": start_iso,
        "window_end_utc": end_iso,
        "tweets_scanned": scanned,
        "tickers": sorted(
            [{"ticker": t, "mentions": c} for t, c in counts.items()],
            key=lambda x: (-x["mentions"], x["ticker"])
        )
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
