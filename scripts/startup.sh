crontab /var/conf/cron.conf

# Start the cron service in the background.
# cron -f &
service cron start

# Start flask server
python app.py
