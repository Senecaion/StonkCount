import os, re, datetime as dt, collections, json, requests

BEARER = os.getenv("X_BEARER_TOKEN")
if not BEARER:
    raise SystemExit("❌  Set X_BEARER_TOKEN environment variable.")

# List of accounts (without @)
HANDLES = ["buzztickr", "allday_stocks", "AltindexApp", "thinknum"]

# Regex for $TSLA, $BRK.B, etc.
CASHTAG_RE = re.compile(r"\$([A-Za-z]{1,5}(?:[.\-][A-Za-z0-9]{1,3})?)\b")

def get_user_id(username):
    r = requests.get(
        f"https://api.twitter.com/2/users/by/username/{username}",
        headers={"Authorization": f"Bearer {BEARER}"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["data"]["id"]

def get_tweets(user_id, start_iso, end_iso):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": 100,
        "start_time": start_iso,
        "end_time": end_iso,
        "tweet.fields": "created_at",
    }
    r = requests.get(url, headers={"Authorization": f"Bearer {BEARER}"}, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("data", [])

def extract_cashtags(text):
    return {m.group(1).upper() for m in CASHTAG_RE.finditer(text or "")}

def main():
    now = dt.datetime.now(dt.timezone.utc)
    start = (now - dt.timedelta(hours=24)).isoformat().replace("+00:00", "Z")
    end = now.isoformat().replace("+00:00", "Z")

    counts = collections.Counter()
    scanned = 0
    for handle in HANDLES:
        try:
            uid = get_user_id(handle)
            tweets = get_tweets(uid, start, end)
            scanned += len(tweets)
            for t in tweets:
                for tag in extract_cashtags(t["text"]):
                    counts[tag] += 1
        except Exception as e:
            print(f"⚠️  Error fetching @{handle}: {e}")

    result = {
        "window_start_utc": start,
        "window_end_utc": end,
        "handles": HANDLES,
        "tweets_scanned": scanned,
        "tickers": sorted(
            [{"ticker": k, "mentions": v} for k, v in counts.items()],
            key=lambda x: (-x["mentions"], x["ticker"]),
        ),
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
