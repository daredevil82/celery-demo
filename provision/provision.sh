#!/bin/bash

# Bash provisioning script to provide functionality for a basic Django appserver and 
# Celery demonstration box
# 
# Responsibile for installing and configuring
# 	* Python 3.x
# 	* Django 1.8.x
# 	* Celery 3.2.x
# 	* MySQL 5.6.x
# 	* RabbitMQ 3.6.x 
# 	* Redis 3.2.x

# Top level shell script values

export DEBIAN_FRONTEND=noninteractive

# set mysql root password without having to use shell


# Django Project Variables

PROJECT_NAME="celerydemo"
APP_NAME="app"
DJANGO_SETTINGS_PATH="project/$PROJECT_NAME/$PROJECT_NAME/settings.py"

DB_USER="dev"
DB_PASS="default123"

echo "Setting MySQL root password"
debconf-set-selections <<< "mysql-server mysql-server/root_password password $DB_PASS"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $DB_PASS"

# RabbitMQ user variables
MQ_USER="admin"
MQ_PASS=$DB_PASS
MQ_VHOST="demo"

# Virtualenv and project location
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME
PROJECT_DIR=/home/vagrant/project

# Add rabbitmq signing key and project repository to aptitude
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list

# Add Redis ubuntu repository for updated binaries
add-apt-repository ppa:chris-lea/redis-server -y

echo "Updating repositiories installed packages"
apt-get update -y
apt-get upgrade -y

echo "Installing dependencies from repositories"
apt-get install -y build-essential python3-pip python3-dev libncurses5-dev libffi-dev libxml2 libxml2-dev libxslt1.1 libxslt1-dev
apt-get install -y mysql-server-5.6 libmysqlclient-dev rabbitmq-server redis-server

echo "Configuring MySQL"
mysql -u root -p$DB_PASS -e "create user '$DB_USER'@'localhost' identified by '$DB_PASS'"
mysql -u root -p$DB_PASS -e "create database `$PROJECT_NAME`"
mysql -u root -p$DB_PASS -e "grant all privileges on `$PROJECT_NAME`.* to '$DB_USER'@'localhost'"
mysql -u root -p$DB_PASS -e "flush privileges"

echo "Configuring RabbitMQ"
rabbitmq-plugins enable rabbitmq_management
echo "Adding RabbitMQ User"
rabbitmqctl add_user $MQ_USER $MQ_PASS
echo "Adding VirtualHost"
rabbitmqctl add_vhost $MQ_VHOST
echo "Setting User Tag"
rabbitmqctl set_user_tags $MQ_USER administrator
echo "Adding User Permissions"
rabbitmqctl set_permissions -p demo $MQ_USER ".*" ".*" ".*"
rabbitmqctl delete_user guest

echo "Checking if virtualenv needs to be installed"
if [[ ! -f /usr/local/bin/virtualenv ]]; then
	echo 'Downloading pip dependencies'
	pip3 install virtualenv stevedore virtualenv-clone virtualenvwrapper
fi

echo "Creating Python virtualenv"
su - vagrant -c "/usr/local/bin/virtualenv --python=/usr/bin/python3 "$VIRTUALENV_DIR" && \
    $VIRTUALENV_DIR/bin/pip3 install -r /home/vagrant/project/requirements.txt"

echo "VIRTUALENVWRAPPER_PYTHON=/usr/bin/python" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc

# Install project db schema
cd "project/$PROJECT_NAME"
./manage.py makemigrations  --no-input
./manage.py migrate --no-input


 





