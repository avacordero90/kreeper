FROM kreeperlabs/kreeper:latest
# this is probably stupid # actually just use a .dockerignore.
COPY ssl/ /root/kreeper/ssl
WORKDIR /root/kreeper
CMD (git stash && git pull && git checkout main &&  && setup/config.sh && kreeper.py) || bash
