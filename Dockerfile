FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get -y install gcc

# RUN apt-get install -y python-pip python-dev



RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

# Install the cron service
# RUN apt-get install cron -y
RUN apt-get -y install python3-dev
RUN apt-get install libffi-dev
ENV PATH /opt/conda/bin:$PATH

RUN pip install --upgrade pip
RUN pip install pystan
#RUN pip install Flask

RUN apt-get -y install libevent-dev
RUN conda install gcc
RUN pip install fbprophet
RUN pip install pyflux


#-------------------------------
# Cron

# Install the cron service
RUN apt-get install cron -y

# Add our crontab file
# ADD cron.conf /var/conf/cron.conf

# Add a cron script file
# ADD cron.sh /var/scripts/cron.sh

# Use the crontab file.
# RUN crontab /var/conf/cron.conf

# RUN service cron start

#-------------------------------
# Requirements

# We copy just the requirements.txt first to leverage Docker cache
# COPY ./requirements.txt /app/requirements.txt

WORKDIR /app/app

# RUN pip install -r requirements.txt

#-------------------------------
# App

# COPY . /app

# ENTRYPOINT ["/tini", "--"]
# ENTRYPOINT [ "python" ]
# CMD [ "app.py" ]

CMD ["/bin/bash", "/app/scripts/startup.sh"]
