#!/bin/bash

echo "initializing kreeper server installation ..."

sleep 1

echo "========================================================"
echo "this installer is for internal use only."
echo "requires debian-based linux and root access."
echo "recommended to install to a container."
echo "========================================================"

echo "continue? Y/n"
read answer

if [[ $answer == 'y'* ]]; then
    cd ~
    rm -rf ~/kreeper/

    sudo apt install git -y

    git clone git@github.com:avacordero90/kreeper.git

    # test that we have git/perms
    if [[ ! $1 ]]; then
        cd ~/kreeper/

        bash <(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)

        echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile
        eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

        brew install python#3.10
        # brew install pip

        

        # if [[ ! $1 ]]; then
        #     sudo rm -rf python.tgz
        #     sudo rm -rf /usr/bin/python3.9

        #     sudo mv ~/kreeper/Python-3.9.6 ~/python3.9 2>/dev/null
            
        #     cd ~/python3.9

        #     sudo make clean

        #     sudo ./configure --prefix=${HOME} --enable-optimizations
            
        #     if [[ ! $1 ]]; then
        #         sudo make && sudo make install

        #         sudo ln -sf ~/python3.9/python /usr/bin/python
        #         sudo ln -sf ~/python3.9/python /usr/bin/python3
        #         sudo ln -sf ~/python3.9/python /usr/bin/python3.9

        #         cd ~/kreeper

        #         curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py

        #         python3.9 get-pip.py

        #         sudo ln -s ~/bin/pip3 /usr/bin/pip
                
        #         # sudo ln -sf ~/python3.9/bin/pip /usr/bin/pip
        #         # sudo ln -sf ~/python3.9/bin/pip3 /usr/bin/pip3
        #         # sudo ln -sf ~/python3.9/bin/pip3.9 /usr/bin/pip3.9

        #         if [[ $1 ]]; then
                
        #             rm -f ~/kreeper/get-pip.py

        #             pip install -U pipenv

        #             if [[ $1 ]]; then
        #                 # pipenv --python /bin/python3.9
        #                 cd ~/kreeper/

        #                 pipenv clean && pipenv shell source ./install/config.sh

        #                 if [[ $1 ]]; then
        #                     pipenv --version && python3.9 ~/kreeper.py --help

        #                     if [[ $1 ]]; then
        #                         echo -e "installation complete!\n"
        #                     else
        #                         echo -e "installation failed: pipenv or python not found.\n"
        #                     fi
        #                 else
        #                     echo -e "installation failed!\n"
        #                 fi
        #             else
        #                 echo -e "installation failed!\n"
        #             fi
        #         else
        #             echo -e "installation failed!\n"
        #         fi
        #     else
        #         echo -e "installation failed!\n"
        #     fi
        # else
        #     echo -e "installation failed!\n"
        # fi
    else
        echo -e "installation failed!\n"
    fi

else
    echo -e "installation aborted!\n"
fi


