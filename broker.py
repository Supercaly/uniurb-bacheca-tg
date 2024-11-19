import feedparser
import requests

# Config
FEED_URL = "feed_url"
BOT_TOKEN = "bot:token"
TG_CHAT_ID = "@chat_id"
TG_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_item_to_tg(item: object, url: str, chat_id: str) -> bool:
    """
    Send a feed item as a message to the telegram channel.

    Params:
        item: The feed item to send.
        url: URL of the tg bot api.
        chat_id: TG chat id.
    
    Returns:
        True if the message is sent correctly, False in case of error.
    """
    text = f"{item.title}"
    res = requests.post(url, data={
        "chat_id": chat_id,
        "text": text
    })
    if not res.ok:
        print(f"ERROR: {res.json()}")
        return False
    return True

# Reed and parse the RSS the feeds
feed = feedparser.parse(FEED_URL)
print(f"got {len(feed.entries)} feeds")

# Send new feeds to tg
for entry in feed.entries:
    send_item_to_tg(entry, TG_URL, TG_CHAT_ID)
