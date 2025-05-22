import feedparser
import requests
import os

RSS_URL = os.environ["RSS_URL"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
STATE_FILE = "latest_post.txt"

feed = feedparser.parse(RSS_URL)
if not feed.entries:
    print("No entries found.")
    exit()

latest_entry = feed.entries[0]
latest_url = latest_entry.link
latest_title = latest_entry.title

# 前回送信したURLを読み込む
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        last_url = f.read().strip()
else:
    last_url = ""

# 新しい投稿があれば通知
if latest_url != last_url:
    message = f"新規投稿だよ: *{latest_title}*\n{latest_url}"
    requests.post(SLACK_WEBHOOK_URL, json={"text": message})

    with open(STATE_FILE, "w") as f:
        f.write(latest_url)
else:
    print("No new posts.")