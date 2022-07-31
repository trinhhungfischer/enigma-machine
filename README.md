# enigma-machine

A Enigma M3 Simulation for Introduction to Information Security Project

# Install requirement and setup environment
You can use pip install directly but I recommend you should use a virtual environment to interact with pip and python. You can easily install requirements by command if you had python and pip.
```
pip install -r requirement.txt
```
However, to avoid some conflicts, you should create a python virtual enviroment and activate it. If this package is not installed, please download Python and [this package](https://pypi.org/project/virtualenv/) with Linux OS.
```
virtualenv .venv
source .venv/bin/activate
```
or to create and activate a virtual environment on Windows, run command
```
python -m venv venv
venv\Scripts\activate.bat
```
After enviroment activation, you must install requirement by this command.
```
.venv/bin/pip install -r requirements.txt
```

or in Window
```
pip install -r requirements.txt
```
# Usage
The simulation app is written by Flask and could played in localhost. You can use it by run [app.py](./app.py) python file by terminal by command in window
```
python app.py
```
or in linux 
```
python3 app.py
```
After that, you can open browser with [127.0.0.1:5000](127.0.0.1:5000) to start simulation app. You can setup rotor, rotor settings or plugboard setting for Enigma M3 simulation machine
