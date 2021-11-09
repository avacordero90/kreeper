#!/bin/bash

echo "initializing kreeper server installation ..."

sleep 1

echo "========================================================"
echo "this installer is for internal use only."
echo "requires git and root access."
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

        curl -s "https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz" -o ~/kreeper/python.tgz && tar -zxvf ~/kreeper/python.tgz

        if [[ ! $1 ]]; then
            sudo rm -rfp python.tgz
            sudo rm -rfp /usr/bin/python3.9

            sudo mv ~/kreeper/Python-3.9.6 /usr/bin/python3.9 2>/dev/null
            cd /usr/bin/python3.9

            sudo make clean

            sudo ./configure --prefix=${HOME}/localpython --enable-optimizations
            
            if [[ ! $1 ]]; then
                sudo make && sudo make install && \
                curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py

                cat ~/.bashrc | grep "usr/bin/python/python3.9"

                if [[ "$(cat ~/.bashrc | grep "usr/bin/python/python3.9")" ]]; then
                    echo -e "# this is to install python3.9\nexport PATH=\$PATH:usr/bin/python/python3.9" >> ~/.bashrc && source ~/.bashrc
                fi
                
                source ~/.bashrc

                ###################################
                # TO DO - continue coding here!!! #
                ###################################

                sudo python3.9 get-pip.py
                
                if [[ $1 ]]; then
                
                    rm -f ~/kreeper/get-pip.py

                    sudo -H pip install -U pipenv

                    if [[ $1 ]]; then
                        # pipenv --python /bin/python3.9
                        cd ~/kreeper/

                        pipenv clean && pipenv shell source ./install/config.sh

                        if [[ $1 ]]; then
                            pipenv --version && python3.9 ~/kreeper.py --help

                            if [[ $1]]; then
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


