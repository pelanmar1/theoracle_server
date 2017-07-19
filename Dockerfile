FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

#-------------------------------
# Cron

# Install the cron service
RUN apt-get install cron -y

# Add our crontab file
ADD cron.conf /var/conf/cron.conf

# Add a cron script file
ADD cron.sh /var/scripts/cron.sh

# Use the crontab file.
RUN crontab /var/conf/cron.conf

RUN service cron start

#-------------------------------
# Requirements

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

#-------------------------------
# App

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
