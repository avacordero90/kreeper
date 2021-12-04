#!/bin/bash

echo "initializing kreeper server configuration ..."


# if [ ! "$BASH_VERSION" ] ; then
#     echo "Please do not use sh to run this script ($0), just execute it directly" 1>&2
#     exit 1
# fi

sleep 1

echo "==========================================================================================================================="
echo "this configurator is for internal use only."
echo "to install all dependencies and then automatically run this script within a virtual environment, run ./install.sh"
echo "==========================================================================================================================="

echo "continue? yes/no"
read answer

if [[ $answer == 'y'* ]]; then
    rm -f /usr/bin/kreeper.py
    ln -s ~/kreeper/kreeper.py /usr/bin/kreeper.py --force
    chmod u+x /usr/bin/kreeper.py

    pip3 install -r ~/kreeper/requirements.txt

    # echo "enter kucoin API key:"
    # read -s KUCOIN_KEY
    # export KUCOIN_KEY=$KUCOIN_KEY

    # echo "enter kucoin API secret: "
    # read -s KUCOIN_SECRET
    # export KUCOIN_SECRET=$KUCOIN_SECRET

    # echo "enter kucoin API passphrase: "
    # read -s KUCOIN_PASSPHRASE
    # export KUCOIN_PASSPHRASE=$KUCOIN_PASSPHRASE

    source ~/.profile

    echo -e "configuration complete!\n"
    echo "you can now run the kreeper service by typing 'kreeper.py'" 
else
    echo -e "configuration aborted!\n"
fi
