# Dochunt

An OSINT tool to run public vk documents though an OCR system.

## Install:
```sh
git clone https://github.com/anatolykopyl/dochunt.git
cd dochunt
pip install -r requirements.txt
```

## Usage:

1. Set up your credentials in `config.ini`.

2. Set up whatever you're interested in in `config.ini` 
in `interests`. This should be either a list of strings
formatted like this:
```ini
interests = [
    "interest1",
    "interest2",
    "interest3",
    ...
  ]
```
If the image contains any of these strings the script will save it.

Or the word `any` to save any image containing text.
```ini
interests = any
```

3. Run the script 

This will watch the latest uploaded document:
```sh
python main.py
```
This will go through all availible documents (vk caps search to 1000 latest docs):
```sh
python main.py -a
```


Inspired by [darkshot](https://github.com/mxrch/darkshot).