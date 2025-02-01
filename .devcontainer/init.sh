#/bin/bash

# fonts
sudo apt update
sudo apt install software-properties-common pipx -y
sudo apt-add-repository contrib -y
sudo apt update
echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections
sudo apt install ttf-mscorefonts-installer -y

# python libraries
pipx install -r requirements.txt

# playwright
playwright install --with-deps webkit