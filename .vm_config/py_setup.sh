#!/bin/sh -e
apt-get update
apt-get -y upgrade
apt-get -qqy install build-essential 
apt-get -qqy install python-dev 
# libreadline6-dev libgdbm-dev zlib1g-dev libbz2-dev
apt-get -qqy install python3 
apt-get -qqy install python3-dev
apt-get -qqy install sqlite3 libsqlite3-dev
# for psycopg2
apt-get -qqy install libpq-dev  
apt-get -qqy install python-pip
pip install --upgrade pip
pip install virtualenv virtualenvwrapper

# mkdir ~/src
# wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
# sudo python ez_setup.py
# sudo easy_install pip

echo alias python=python3 >> ~/.bash_aliases

# echo "if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then" >> ~/.bash_rc
# echo "    export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bash_rc
# echo "    source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_rc
# echo "fi" >> ~/.bash_rc

. ~/.bashrc

# cd /mnt/tournament
# virtualenv venv
# . venv/bin/activate
# pip install -r requirements.txt

echo
echo "Done provisioning, now:"
echo "  ==> vagrant ssh"
echo "  ==> cd /mnt/karma"

# mkvirtualenv dev
# workon dev
# deactivate