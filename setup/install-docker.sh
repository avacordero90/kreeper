#!/bin/bash

echo "initializing kreeper server installation ..."

sleep 1

echo "========================================================"
echo "this installer is for internal use only."
echo "requires debian-based linux and root access."
echo "recommended to install to a vm or docker container."
echo "========================================================"

echo "continue? yes/no"
read answer

if [[ $answer == 'y'* ]]; then
    cd ~
    rm -rf ~/kreeper/ /kreeper/

    apt update && \
        apt install -y curl git python3 python3-pip

    git clone git@github.com:avacordero90/kreeper.git
    
    source ~/.profile

    # pipenv shell source ~/kreeper/setup/config.sh
    source ~/kreeper/setup/config.sh

    # if [[ $1 ]]; then
        # pipenv --version

        if [[ $1 ]]; then
            echo -e "installation complete!\n"
        else
            echo -e "installation failed: unknown error.\n"
        fi
    # else
    #     echo -e "installation failed!\n"
    # fi

else
    echo -e "installation aborted!\n"
fi


