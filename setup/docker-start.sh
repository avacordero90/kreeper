#!/bin/bash

sudo docker build -t kreeper ~/kreeper && \
    sudo docker run -p 0.0.0.0:443:443/tcp -e SSL_PASSPHRASE=$ssl_pp -it kreeper