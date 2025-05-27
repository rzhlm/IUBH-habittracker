# Habit Tracker project for IUBH

## Table of Contents

### [Screenshots](#Screenshots)
### [Installing](#Installing)
#### [Dependencies](#Dependencies)
#### [Option 1: clone and run](#option-1-clone-and-run)
#### [Option 2: download packaged binaries](#option-2-download-packaged-binaries)
#### [Option 3: (unstable) install from 'pyproject.toml'](#option-3-unstable-install-from-pyprojecttoml)
### [Using the software](#using-the-software)

## Screenshots
screenshots

## Installing

### Dependencies
For the program itself there are no dependencies, other than the Python Standard Library

For testing, Pytest is used (>= 8.3.3).

Python >= 3.13.0 is required, as the new syntax regarding type hints is used.

### Option 1: clone and run
1) Make sure you have a Python version >= 3.13.0
   
e.g. if using Pyenv for version management:
 ```
pyenv install 3.13.3
```
e.g. with 'uv':
```
uv python install 3.13
```

2) Clone the project


 ```
git clone https://github.com/rzhlm/IUBH-habittracker.git
cd IUBH-habittracker
 ```
**a) if you don't want to run any testing, then you don't need to install anything further.**

simply run it:
```
python main.py
```
**b) if you would like to run the testing, you need to install PyTest**

it is recommended to make a virtual environment.

e.g. with Python directly:
```
python -m venv venv --prompt HabitTracker
.\venv\Scripts\activate.bat (on Windows)
source /venv/bin/activate (POSIX)
```
or with the equivalent options in 'uv' or 'pyenv', or whichever tools you use.
Once that is done, you can install the required PyTest package:
```
uv pip install -r requirements.txt
or 
pip install -r requirements.txt
```

and then you can run the tests, e.g.
```
pytest .
or
pytest -v .
```


### Option 2: Download a packaged binary release
This has only been tested on local development machines: 

Even though they are packaged for standalone use, it could be that particular dependencies are needed on your device.

Windows (x64): (here)

macOS (Apple ARM): (here)


### Option 3: (unstable) install from 'pyproject.toml'

e.g. with 'uv': 
```
uv pip install .[test]
```
e.g. with 'pip': 
```
pip install .[test]
```

## Using the software
placeholder

