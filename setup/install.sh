#!/bin/bash

echo "initializing kreeper server installation ..."

sleep 1

echo "========================================================"
echo "this installer is for internal use only."
echo "requires git."
echo "========================================================"

echo "continue? Y/n"
read answer

if [[ $answer == 'y'* ]]; then
    cd ~
    rm -rf ~/kreeper/
    git clone git@github.com:avacordero90/kreeper.git

    cd ~/kreeper/
    curl -X GET "https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz" --output python.tgz && tar -zxvf python.tgz
    sudo rm -rf python.tgz

    cd ~/kreeper/Python-3.9.6
    sudo make clean && sudo /configure --prefix=${HOME}/localpython --enable-optimizations
    sudo make && sudo make install

    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    pip --python /usr/bin/python3

    sudo python get-pip.py
    rm -f ~/kreeper/get-pip.py

    sudo -H pip install -U pipenv
    # pipenv --python /bin/python3.8

    cd ~/kreeper/
    pipenv clean
    
    pipenv shell source ./install/config.sh

    if [[ $(pipenv --version) ]]; then
        echo -e "installation complete!\n"

        ~/kreeper/setup/config.sh
    else
        echo -e "installation failed!\n"
    fi

else
    echo -e "installation aborted!\n"
fi


