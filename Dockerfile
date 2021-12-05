FROM kreeperlabs/kreeper:latest

COPY ssl/ /root/kreeper/ssl
WORKDIR /root/kreeper

CMD (git checkout main && \
        git stash && \
        git pull && \
        setup/kreeper-config.sh && \
        SSL_PASSPHRASE=$SSL_PASSPHRASE kreeper.py) & \
            bash

