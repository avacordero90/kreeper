#!/bin/bash

rm -rf ~/kreeper/ssl
mkdir ~/kreeper/ssl

# ssh-keygen -t rsa -C $(hostname) -f "~/.ssh/id_rsa" -P "" && cat ~/.ssh/id_rsa.pub
openssl req -x509 -newkey rsa:4096 -keyout ~/kreeper/ssl/key.pem -out ~/kreeper/ssl/cert.pem -sha256 -days 365 -subj "/C=US/ST=California/L=San Diego/O=Kreeper Labs/OU=Engineering/CN=api.kreeper.trade"


# sudo docker build -t kreeper . && sudo docker run -p 0.0.0.0:443:443/tcp -it kreeper