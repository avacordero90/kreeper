#!/bin/bash

echo "initializing kreeper server installation ..."

sleep 1

echo "========================================================"
echo "this installer is for internal use only."
echo "requires debian-based linux and root access."
echo "recommended to install to a container."
echo "========================================================"

echo "continue? yes/no"
read answer

if [[ $answer == 'y'* ]]; then
    cd ~
    rm -rf ~/kreeper/

    sudo apt install git -y

    git clone git@github.com:avacordero90/kreeper.git

    cd ~/kreeper

    echo -e "\n" | bash <(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)

    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

    brew install python@3.10
    
    export PATH=$PATH:/home/linuxbrew/.linuxbrew/opt/python@3.10/bin
    source ~/.profile 

    pip3 install pipenv

    rm -f ~/kreeper/Pipfile

    pipenv clean

    ln -s ~/kreeper/kreeper.py /home/linuxbrew/.linuxbrew/bin/kreeper.py --force
    chmod u+x /home/linuxbrew/.linuxbrew/bin/kreeper.py
    source ~/.profile

    pipenv shell source ~/kreeper/setup/config.sh

    if [[ $1 ]]; then
        pipenv --version

        if [[ $1 ]]; then
            echo -e "installation complete! Moving on\n"
        else
            echo -e "installation failed: pipenv or python not found.\n"
        fi
    else
        echo -e "installation failed!\n"
    fi

else
    echo -e "installation aborted!\n"
fi


