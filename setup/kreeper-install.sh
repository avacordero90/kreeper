#!/bin/bash

echo "initializing kreeper server installation ..."

sleep 1

echo "========================================================"
echo "this installer is for internal use only."
echo "requires debian-based linux and root access."
echo "recommended to install to a vm or docker container."
echo "========================================================"

cp -r $(dirname "$0")/.. ~/kreeper && cd ~/kreeper

apt update && \
    apt install -y python3 python3-pip

source ~/kreeper/setup/kreeper-config.sh

echo "configuration complete!"
echo "you can now run the kreeper service by typing 'kreeper.py'"
echo "starting kreeper.py now..."
sleep 1
 
kreeper.py
