import feedparser
import requests
import os
import datetime

RSS_URL = os.environ["RSS_URL"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
STATE_FILE = "latest_post.txt"

feed = feedparser.parse(RSS_URL)
if not feed.entries:
    print("No entries found.")
    exit()


# 前回送信した時間を読み込む
last_time = datetime.datetime.min
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        try:
            last_time = datetime.datetime.fromisoformat(f.read().strip())
        except Exception as e:
            print("invalid time record. use min time")



# 新しい投稿があれば通知
new_entries = [
    entry for entry in feed.entries
    if datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)>last_time
]
for entry in reversed(new_entries):
    message = f"新規投稿だよ: *{entry.title}*\n{entry.link}"
    print(f"{entry.title}:{entry.link}")
    requests.post(SLACK_WEBHOOK_URL, json={"text": message, "unfurl_links": True})

now = datetime.datetime.now(datetime.timezone.utc)
with open(STATE_FILE, "w") as f:
    f.write(now.isoformat())
