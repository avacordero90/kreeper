#!/bin/bash

echo -e "Enter your PEM passphrase: "
read -s ssl_pp

~/kreeper/setup/docker-cleanup.sh
~/kreeper/setup/docker-config-dev.sh
~/kreeper/setup/docker-start.sh