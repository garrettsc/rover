#Create virutal environment
echo $'\n######### Creating virtual environment #########\n'
python3 -m venv ~/py3_env

#Activate the environment
echo $'\n######### Activating environment #########\n'
source ~/py3_env/bin/activate

echo $'\n######### Installing Python dependencies #########\n'
pip3 install pyzmq PySide2
