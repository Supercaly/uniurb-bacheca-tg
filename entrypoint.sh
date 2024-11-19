#! /bin/bash

# Create crontab file with given pattern
echo "running app with cron pattern '${CRON_PATTERN}'"
echo "${CRON_PATTERN} /usr/local/bin/python /app/broker.py > /proc/1/fd/1 2>&1" > "/etc/cron.d/crontab"
/usr/bin/crontab /etc/cron.d/crontab

# Copy current environment for cron
printenv > /etc/environment

# Run cron in foreground mode
cron -f -l 2
