#/bin/bash

# python libraries
pip install -r requirements.txt

# fonts
sudo apt update
sudo apt install software-properties-common -y
sudo apt-add-repository contrib -y
sudo apt update
echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections
sudo apt install ttf-mscorefonts-installer -y

# playwright
playwright install --with-deps webkit