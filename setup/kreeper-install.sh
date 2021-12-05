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
    cp -r $(dirname "$0")/.. ~/kreeper && cd ~/kreeper
#     rm -rf ~/kreeper/ /kreeper/

    apt update && \
        apt install -y python3 python3-pip

    rm -f /usr/bin/kreeper.py
    ln -s ~/kreeper/kreeper.py /usr/bin/kreeper.py --force
    chmod u+x /usr/bin/kreeper.py

    pip3 install -r ~/kreeper/requirements.txt

    echo "configuration complete!"
    echo "you can now run the kreeper service by typing 'kreeper.py'"
    echo "starting kreeper.py now..."
    sleep 1

else
    echo -e "installation aborted!\n"
fi


