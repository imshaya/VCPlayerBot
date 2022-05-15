sudo apt-get -y purge python3.8 && sudo apt-get -y autoremove
wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz && tar xzf Python-3.9.9 && cd Python-3.9.9 && sudo ./configure --enable-optimizations && sudo make altinstall
