import os
import logging
import feedparser
import requests
from html2text import HTML2Text

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

def send_item_to_tg(
    title: str,
    desc: str,
    link: str,
    url: str,
    chat_id: str
) -> bool:
    """
    Send a feed item as a message to the telegram channel.

    Params:
        title: Title of the feed item to send.
        desc: Description of the feed item to send.
        link: Link to the feed item to send.
        url: URL of the tg bot api.
        chat_id: TG chat id.
    
    Returns:
        True if the message is sent correctly, False in case of error.
    """
    text = f"{title}\n\n{desc}\n{link}"
    res = requests.post(url, data={
        "chat_id": chat_id,
        "text": text
    })
    if not res.ok:
        logging.getLogger(__name__).error(res.json())
        return False
    return True

def main():
    # Get logger
    logger = logging.getLogger(__name__)

    # Global html2text converter
    h2t = HTML2Text()

    # Get configs from env variables
    DB_FOLDER = get_env('DB_FOLDER')
    DB_FILE = get_env('DB_FILE')
    DB_PATH = os.path.join(DB_FOLDER, DB_FILE)
    FEED_URL = get_env('FEED_URL')
    TG_BOT_TOKEN = get_env('TG_BOT_TOKEN')
    TG_CHAT_ID = get_env('TG_CHAT_ID')
    TG_URL = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"

    # Read db file
    try:
        with open(DB_PATH, 'r') as db:
            old_msgs = db.readlines()
            old_msgs = list(map(lambda e: e.replace("\n",""), old_msgs))
    except IOError:
        old_msgs = []
    logger.info(f"got {len(old_msgs)} old messages")

    # Reed and parse the RSS the feeds
    feed = feedparser.parse(FEED_URL)
    logger.info(f"got {len(feed.entries)} items from feed")

    # Get all items that where not sent previously
    items_to_send = [i for i in feed.entries if i.link not in old_msgs]
    items_to_send.reverse()
    logger.info(f"need to send {len(items_to_send)} items")

    # Send new items to tg
    new_msgs = []
    for entry in items_to_send:
        if send_item_to_tg(entry.title,
                        h2t.handle(entry.description),
                        entry.link,
                        TG_URL,
                        TG_CHAT_ID):
            new_msgs.append(entry.link)
    logger.info(f"sent {len(new_msgs)} items")

    # Append the id the the sent items to the db
    with open(DB_PATH, "a+") as db:
        for i in new_msgs:
            db.write(i)
            db.write("\n")

if __name__ == "__main__":
    # Init logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s: %(message)s"
    )
    logger = logging.getLogger(__name__)

    try:
        main()
    except Exception as ex:
        logger.error(ex)
