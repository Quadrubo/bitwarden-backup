#!/bin/sh
if [ -z "$CRON_SCHEDULE" ]; then
  export CRON_SCHEDULE='0 0 * * *'
fi

echo "CRON_SCHEDULE: $CRON_SCHEDULE"

# Run substitutions on the template file and inject the crontab
envsubst < /app/crontab.template | crontab