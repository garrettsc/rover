#Create virutal environment
echo $'\n######### Creating virtual environment #########\n'
python3 -m venv ~/py3_env

#Activate the environment
echo $'\n######### Activating environment #########\n'
source ~/py3_env/bin/activate

#Install gpio library
echo $'\n######### Installing GPIO Python Library #########\n'
pip3 install gpiozero RPi.GPIO pyzmq


# Add the following to crontab
#
# @reboot /home/pi/.../run.sh where run.sh executes the 
# camera and motor command scripts
