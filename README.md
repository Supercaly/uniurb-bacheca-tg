# Uniurb RSS to Telegram channel

This python code creates a server that listens periodically to RSS feeds created by the "bacheca" of "INFORMATICA - SCIENZA E TECNOLOGIA" at Uniurb and sends them to a dedicated telegram channel.

## Setup

This app is deployed using docker compose.
Use the `docker-compose.yml` file provided with this repository and run it with

```terminal
$ docker compose up -d
```

## Environment Variables

This app uses the following environment variables

- `DB_FOLDER` (db) folder where the local db is stored
- `DB_FILE` (db.txt) file where the local db is stored
- `FEED_URL` URL for the feed to listen
- `TG_BOT_TOKEN` Token for the telegram BOT that relays the messages
- `TG_CHAT_ID` Telegram chat ID
- `CRON_PATTERN` Crontab pattern used to schedule running the app
