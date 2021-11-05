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

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt install python python3
    elif [[ "$OSTYPE" == "darwin"* ]]; then 
        if [[ ! $(python3 --version) ]]; then
            cd ~/kreeper
            curl https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz > tar -zxvf Python-3.9.6.tgz
            cd Python-3.9.6
            sudo make clean
            sudo /configure --prefix=${HOME}/localpython --enable-optimizations
            sudo make
            sudo make install
        fi
    else
        echo "for real bitch, windows??? ugh."
        sleep 1
        echo "incompatible."
        sleep 1
        echo "fail."
        sleep 1
        echo "bye."
        sleep 1
        exit
    fi

    if [[ ! $(pip3 --version) ]]; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py | python3
    fi

    sudo -H pip install -U pipenv
    cd ~/kreeper/install/

    pipenv clean
    pipenv shell source ./install/config.sh
    
    echo -e "installation complete!\n"
else
    echo -e "installation aborted!\n"
fi


