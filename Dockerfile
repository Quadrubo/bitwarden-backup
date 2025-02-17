FROM python:3.12-slim-bookworm AS builder
ARG S6_OVERLAY_VERSION=3.2.0.0

RUN apt-get update && \
    apt-get install -y xz-utils unzip curl

# Download the bitwarden-cli
WORKDIR /tmp

RUN curl -L "https://github.com/bitwarden/clients/releases/download/cli-v2025.1.3/bw-linux-2025.1.3.zip" -o bw.zip \
    && unzip bw.zip

# Download s6-overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp

FROM python:3.12-slim-bookworm

# Install the necessary packages
# cron: to run the cron job
# gettext: to use envsubst
RUN apt-get update && \
    apt-get install -y cron gettext xz-utils

# Install bitwarden-cli
COPY --from=builder /tmp/bw /usr/local/bin/bw
RUN chmod +x /usr/local/bin/bw

# Install s6-overlay
COPY --from=builder /tmp/s6-overlay-noarch.tar.xz /tmp/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src .

# Copy the cron job template file
COPY docker/crontab.template /app/crontab.template

# Copy the s6-overlay files
COPY docker/etc/s6-overlay /etc/s6-overlay

# make all files in /etc/s6-overlay/scripts executable
RUN find /etc/s6-overlay/scripts -type f -exec chmod +x {} \;

ENTRYPOINT ["/init"]