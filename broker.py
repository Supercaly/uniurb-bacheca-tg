import feedparser
import requests
import os

def get_env(env: str) -> str:
    """
    Read the vale of given environment variable or throw an error.

    Params:
        env: Name of the env variable to load.
    """
    val = os.getenv(env)
    if val == None:
        raise Exception(f"environment variable '{env}' not defined")
    return val

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

def main():
    # Get configs from env variables
    FEED_URL = get_env('FEED_URL')
    TG_BOT_TOKEN = get_env('TG_BOT_TOKEN')
    TG_CHAT_ID = get_env('TG_CHAT_ID')
    TG_URL = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"

    print(f"{FEED_URL     = }")
    print(f"{TG_BOT_TOKEN = }")
    print(f"{TG_CHAT_ID   = }")
    print(f"{TG_URL   = }")

    # Reed and parse the RSS the feeds
    feed = feedparser.parse(FEED_URL)
    print(f"got {len(feed.entries)} feeds")

    # Send new feeds to tg
    for entry in feed.entries:
        send_item_to_tg(entry, TG_URL, TG_CHAT_ID)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"ERROR: {ex}")