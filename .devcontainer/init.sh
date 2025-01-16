#/bin/bash

# python libraries
pip install -r requirements.txt

# fonts
sudo apt update
sudo apt install fonts-noto -y

# playwright
playwright install --with-deps webkit