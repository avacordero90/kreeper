#!/bin/bash

# ssh-keygen -t rsa -C $(hostname) -f "~/.ssh/id_rsa" -P "" && cat ~/.ssh/id_rsa.pub
# openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -sha256 -days 365 -subj "/C=US/ST=California/L=San Diego/O=Kreeper Labs/OU=Engineering/CN=api.kreeper.trade"
echo -e "Enter your PEM passphrase: "
read ssl_pp

sudo docker build -t kreeper ~/kreeper && \
    sudo docker run -p 0.0.0.0:443:443/tcp -e SSL_PASSPHRASE=$ssl_pp -it kreeper