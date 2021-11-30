FROM kreeperlabs/kreeper:latest
# this is probably stupid # actually just use a .dockerignore.
# COPY ssl/ /root/kreeper/ssl/
WORKDIR /root/kreeper
CMD bash