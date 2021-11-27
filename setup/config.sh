#!/bin/bash

echo "initializing kreeper server configuration ..."

sleep 1

echo "==========================================================================================================================="
echo "this configurator is for internal use only."
echo "it will connect to an API key on a given kucoin account, therefore binding it."
echo "this means calling this kreeper instance may trigger crypto trades with your account. USE WITH CAUTION."
echo "only use this configurator within a python virtual environment."
echo "to install all dependencies and then automatically run this script within a virtual environment, run ./install.sh"
echo "==========================================================================================================================="

echo "continue? yes/no"
read answer

if [[ $answer == 'y'* ]]; then
    
    yes | pip install -r ~/kreeper/requirements.txt

    echo "enter kucoin API key:"
    read -s KUCOIN_KEY
    export KUCOIN_KEY=$KUCOIN_KEY

    echo "enter kucoin API secret: "
    read -s KUCOIN_SECRET
    export KUCOIN_SECRET=$KUCOIN_SECRET

    echo "enter kucoin API passphrase: "
    read -s KUCOIN_PASSPHRASE
    export KUCOIN_PASSPHRASE=$KUCOIN_PASSPHRASE

    echo -e "configuration complete!\n"
    echo "you can now run the kreeper service by typing 'kreeper.py'" 
    kreeper.py --help
    exit 1
else
    echo -e "configuration aborted!\n"
fi
