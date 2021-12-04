FROM kreeperlabs/kreeper:latest

COPY ssl/ /root/kreeper/ssl
WORKDIR /root/kreeper

CMD git checkout main > /dev/null && \
    git stash > /dev/null && \
    git pull > /dev/null && \
    setup/kreeper-config.sh > /dev/null && \
    kreeper.py
