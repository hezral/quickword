<div align="center">

![icon](data/icons/com.github.hezral.quickword.svg)

# ![logo_type](data/logo_type.png?raw=true)
### Quickly lookup words on the fly 

</div>

| ![Screenshot](data/screenshot-01.png?raw=true) | ![Screenshot](data/screenshot-02.png?raw=true) |
|------------------------------------------|-----------------------------------------|

## Demo
![](data/demo.gif)

## Installation

# Install it from source
You can of course download and install this app from source.

## Dependencies
Ensure you have these dependencies installed. 

* python3
* python3-gi
* python3-nltk
* libgranite-dev
* libgtk-3-dev
* espeak

## Installation
Download the updated source [here](https://gitlab.com/hezral/quickword/archive/master.zip), or use git:
```bash
git clone https://gitlab.com/hezral/quickword.git
cd quickword
```

### From .setup.py
In the quickword file directory:
```bash
sudo python3 setup.py install --prefix=/usr --install-data prefix/share --install-purelib prefix/share
sudo python3 post_install.py
```

## Uninstallation
This will output all the installed files.
```bash
sudo python3 setup.py install --prefix=/usr --install-data prefix/share --record files.txt
```
Then when you want to uninstall it simply run; be careful with the 'sudo'
```bash
cat files.txt | xargs sudo rm -rf
```

## Thanks/Credits

- [Ideogram](https://appcenter.elementary.io/com.github.cassidyjames.ideogram/) Inspired by it. Also borrowed/forked some code.
- [ElementaryPython](https://github.com/mirkobrombin/ElementaryPython) This started me off on coding with Python and GTK. 