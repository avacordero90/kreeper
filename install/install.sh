#!/bin/bash

echo "initializing kreeper server installation ..."

sleep 1

echo "========================================================"
echo "this installer is for internal use only."
echo "========================================================"

echo "continue? Y/n"
read answer

if [[ $answer == 'y'* ]]; then
    mkdir ~/kreeper

    if [[ ! $(python3 --version) ]]; then
        cd ~/kreeper
        curl https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz > tar -zxvf Python-3.9.6.tgz
        cd Python-3.9.6
        sudo make clean
        sudo /configure --prefix=${HOME}/localpython --enable-optimizations
        sudo make
        sudo make install
    fi

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
    else
        echo -e "installation failed!\n"
    fi

else
    echo -e "installation aborted!\n"
fi


