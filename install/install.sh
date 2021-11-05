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
        # sudo apt install python python3 -y
        sudo apt install software-properties-common -y
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt update -y
        sudo apt install python3.9 python3.9-distutils -y
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

    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py -o get-pip.py | sudo python3.9

    sudo -H pip install -U pipenv
    cd ~/kreeper/install/

    pipenv clean
    pipenv shell source ./install/config.sh
    
    if [[ pipenv --version ]]; then
        echo -e "installation complete!\n"
    else
        echo -e "installation failed!\n"
    fi

else
    echo -e "installation aborted!\n"
fi


