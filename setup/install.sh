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

    # test that we have git/perms
    if [[ ! $1 ]]; then
        cd ~/kreeper/

        curl -s "https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz" -o python.tgz && tar -zxvf python.tgz

        if [[ ! $1 ]]; then
            sudo rm -rf python.tgz

            cd ~/kreeper/Python-3.9.6
            sudo make clean

            sudo ./configure --prefix=${HOME}/localpython --enable-optimizations
            
            if [[ ! $1 ]]; then
                
                if [[ $(sudo make && sudo make install && \
                curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
                sudo python get-pip.py) ]]; then
                
                    rm -f ~/kreeper/get-pip.py

                    if [[ $(sudo -H pip install -U pipenv) ]]; then
                        # pipenv --python /bin/python3.9

                        cd ~/kreeper/
                        if [[ $(pipenv clean && pipenv shell source ./install/config.sh) ]]; then

                            if [[ $(pipenv --version) ]]; then
                                echo -e "installation complete!\n"
                            else
                            # TO DO: this goes somewhere else
                                echo -e "installation failed: pipenv not found.\n"
                            fi
                        else
                            echo -e "installation failed!\n"
                        fi
                    else
                        echo -e "installation failed!\n"
                    fi
                else
                    echo -e "installation failed!\n"
                fi
            else
                echo -e "installation failed!\n"
            fi
        else
            echo -e "installation failed!\n"
        fi
    else
        echo -e "installation failed!\n"
    fi

else
    echo -e "installation aborted!\n"
fi


