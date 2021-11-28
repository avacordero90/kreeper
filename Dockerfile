FROM kreeper:kreeper
COPY . /kreeper
WORKDIR /kreeper
CMD kreeper.py