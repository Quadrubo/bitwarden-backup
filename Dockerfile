FROM python:3.12-bookworm
ARG S6_OVERLAY_VERSION=3.2.0.0

# Install the necessary packages
# cron: to run the cron job
# xz-utils: to extract the s6-overlay
RUN apt-get update && \
    apt-get install -y cron xz-utils

# ___APP___

# Install bitwarden-cli
WORKDIR /usr/local/bin

RUN curl -L "https://github.com/bitwarden/clients/releases/download/cli-v2024.6.0/bw-linux-2024.6.0.zip" -o bw.zip \
    && unzip bw.zip \
    && chmod +x bw

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY src .

# ___APP___

# Copy the cron job file
ADD docker/crontab.txt /etc/cron.d/main
RUN chmod 0600 /etc/cron.d/main

# Install s6-overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

# Copy the s6-overlay files
COPY docker/etc/s6-overlay /etc/s6-overlay

ENTRYPOINT ["/init"]