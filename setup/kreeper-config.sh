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

# echo "continue? yes/no"
# read answer

rm -f /usr/bin/kreeper.py
ln -s ~/kreeper/kreeper.py /usr/bin/kreeper.py --force
chmod u+x /usr/bin/kreeper.py

pip3 install -r ~/kreeper/requirements.txt

if [[ $1 ]]; then
    echo "configuration complete!"
    echo "you can now run the kreeper service by typing 'kreeper.py'" 
else
    echo "installation failed. please check manually and try again."
fi