#!/bin/bash

rm -rf ~/kreeper/ssl
mkdir ~/kreeper/ssl

openssl req \
    -x509 -newkey rsa:4096 -keyout ~/kreeper/ssl/key.pem \
    -out ~/kreeper/ssl/cert.pem -sha256 -days 365 \
    -subj "/C=US/ST=California/L=San Diego/O=Kreeper Labs/OU=Engineering/CN=api.kreeper.trade"
