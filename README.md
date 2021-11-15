# FourGuys Bank

* ./haarcascade/haarcascade_frontalface_default.xml
* ./main.py

## VirtualBox

download virtualbox and extention
website : https://www.virtualbox.org/wiki/Downloads

## MySQL

website : https://ubuntu.com/server/docs/databases-mysql

### Installation

```
sudo apt-get update && sudo apt-get upgrade && sudo apt-get install mysql-server
systemctl is-active mysql
systemctl is-enabled mysql
sudo mysql_secure_installation
sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '!@#$%^&*()qwertyuiopWinter2021';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SET GLOBAL max_connections = 8192;

sudo systemctl restart mysql.service
```

# Initialize
```
sudo mysql -u root -p !@#$%^&*()qwertyuiopWinter2021 < init.sql
```

## Python

### Update

```
sudo apt-get update && sudo apt-get upgrade
sudo apt install python3-pip

sudo apt install python3-flask
pip3 install flask
pip3 install opencv-python
pip3 install opencv-contrib-python
pip3 install mysql-connector-python
```

## Initialization

```
rm -rf data
mkdir data
mysql -u root -p iKYC < init.sql
```

## Execute

```
export FLASK_APP=main
export FLASK_ENV=development
flask run
```
`