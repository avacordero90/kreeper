FROM kreeperlabs/kreeper:latest
COPY ssl/ /ssl/
WORKDIR /root/kreeper
CMD bash