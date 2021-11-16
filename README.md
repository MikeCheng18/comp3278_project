# FourGuys Bank

## Initialize using Virtual Box
1. download FourGuysBank at https://drive.google.com/file/d/1mV5K8axxxDjWQZWKorD9w8q_SgxXLqUn/view?usp=sharing
2. download the Oracle Virtual Box 6.1.28 and its **extention** at https://www.virtualbox.org/wiki/Downloads 
3. Open the Virtual Box and **import** FourGuysBank
4. Make sure your camera is on (Devices -> Webcam)
5. run `./run.sh` to execute the program and access http://127.0.0.1:5000

### Solution on potential errors
1. If you encountered "failed to open a session for the virtual machine" error, reinstall Oracle Virtual Box 6.1.26 (older version) and its extention at https://www.virtualbox.org/wiki/Download_Old_Builds_6_1
2. For Mac OS users, you may need to grant permission to the software during installation. (System Preferences -> Security & Privacy -> General -> Allow Oracle to load) (more information in the video)

### Other information
#### Ubuntu
Username : comp3278  
Password : comp3278
#### MySQL
Username : root  
Password : !@#$%^&*()qwertyuiopWinter2021

## Training face recognition model
If you want to run the face recognition to register your faceID, you have to 
1. register your face at the home page of FourGuysBank.
2. Train the face recognition AI using the command `python3 train.py`  
    (Manually terminate the training using Ctrl + C if it is too lag later on since it runs in a forever loop)
3. Login at the home page with your faceID.

## Build from scratch
### VirtualBox
download **virtualbox** and **extention**
website : https://www.virtualbox.org/wiki/Downloads

### MySQL

website : https://ubuntu.com/server/docs/databases-mysql

#### Installation
```
sudo apt-get update && sudo apt-get upgrade && sudo apt-get install mysql-server

sudo mysql_secure_installation

sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '!@#$%^&*()qwertyuiopWinter2021';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

sudo systemctl restart mysql.service
```

#### Initialize
```
sudo mysql -u root -p < init.sql
```

### Python

#### Update
```
sudo apt-get update && sudo apt-get upgrade
sudo apt install python3-pip

sudo apt install python3-flask
pip3 install flask
pip3 install opencv-python
pip3 install opencv-contrib-python
pip3 install mysql-connector-python
```

### Initialization
```
rm -rf data
mkdir data
mysql -u root -p < init.sql
```

## Execute

```
export FLASK_APP=main
export FLASK_ENV=development
flask run
```
`
or
```
chmod u+x ./run.sh
./run.sh
```
