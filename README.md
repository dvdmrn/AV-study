# AV-study
Analysing and editing signals with viapoints. Original code by Eduardo Starling.

## Dependencies 
- Python 2.7
- a unix-like environment

## Setting up the software:
You need the following packages to run the software. This section will show you the easiest way to install them using the pip package manager.

- **numpy**: `pip install numpy` 
- **matplotlib** & **scipy**: `pip install scipy matplotlib`
- **pygame** `pip install pygame` (note linux users may have to: `sudo apt-get install python-pygame`)
- **PyQt4**:
    - Install **SIP**:
        - https://riverbankcomputing.com/software/sip/download
        - Unpack the source file 
        - Locate where the folder has been unpacked 
        - Shift and right click an empty space in the folder and open in terminal 
        - `cd` into the folder that contains configure.py 
        - `python configure.py`
    - Install **PyQt4**:
        - using apt-get: `sudo apt-get install python-qt4`
        - OR manual install:
        - Download PyQt at: https://riverbankcomputing.com/software/pyqt/download
        - `cd` in to downloaded folder with a makefile and in terminal run `make`.
        - `make install`
- **PyQt4.phonon**: `sudo apt-get install Python-qt4.phonon`
- **pytables**: `Sudo apt-get install python-tables` (Need to use apt-get due to problems with pip as of 2017.01.30) 
- **posix_ipc**:   
        - Download the tarball: https://pypi.python.org/pypi/posix_ipc  
        - Once extracted, navigate into the folder and type `python setup.py install`.
- **pyaudio**: `sudo apt-get install python-pyaudio` OR...
- **cython**: `sudo pip install cython`
- **scikits.audiolab**: `sudo pip install scikits.audiolab`  
- **gizeh**:  
        - `sudo apt-get install python-dev python-pip ffmpeg libffi-dev`
        - `sudo pip install gizeh`

### More detailed setup information
...can be found over here: https://docs.google.com/document/d/1Ax7sCXPPS9O5m3p_vUgyfT0UCy6QWxxQchM2W7FMrCY/edit?usp=sharing1
