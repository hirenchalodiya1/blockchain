# Run code
![](https://img.shields.io/badge/Ubuntu-lightblue.svg) ![](https://img.shields.io/badge/Python-3.8-blue.svg)
## Required
- python3
- pip
### Install venv, if already not installed
```
sudo apt-get install python3-venv
```
### Create virtual environment
```
python3 -m venv env
./env/bin/activate
pip install -r requirnment.txt
```

### Run code
- If you want 15 nodes then run this in different 15 terminals
```
python node.py -p [port_number]
```
