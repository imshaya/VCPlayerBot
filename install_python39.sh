sudo apt-get -y purge python3.8 && sudo apt-get -y autoremove
sudo apt update && sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9
python3.9 --version


