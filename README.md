<div align="center">

![icon](data/icons/com.github.hezral.quickword.svg)

# ![logo_type](data/logo_type.png?raw=true)
</div>

### Quickly lookup words on the fly and offline
* On the fly word lookup
* Works offline (first run will require internet to download dictionary data)
* Copy definitions and examples to clipboard with just a click
* Word definitions
* Examples of word sentences
* Synonyms
* Explore synonyms from each word

| ![Screenshot](data/screenshot-01.png?raw=true) | ![Screenshot](data/screenshot-02.png?raw=true) |
|------------------------------------------|-----------------------------------------|

## Demo and How to use
QuickWord can be used by manual lookup and via a keyboard shortcut to open it on the fly. 

Select a word and hit the ⌘ + Ctrl + D shortcut to get the lookup.  
* Manual entry of words
* Selecting a text

![](data/demo.gif)

## Installation

### Install from deb file
Download the deb file from the Releases page and install using a deb installer or command line. 
```bash
sudo apt install /path/to/deb/filename.deb
```

### Install it from source
You can of course download and install this app from source.

### Dependencies
Ensure you have these dependencies installed. 

* python3
* python3-gi
* python3-nltk
* libgranite-dev
* libgtk-3-dev
* espeak

### Installation
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
- [Wordnet](http://wordnetweb.princeton.edu/perl/webwn) Definitions are based on Wordnet.
- [Ideogram](https://appcenter.elementary.io/com.github.cassidyjames.ideogram/) Inspired by it. Also borrowed/forked some code.
- [ElementaryPython](https://github.com/mirkobrombin/ElementaryPython) This started me off on coding with Python and GTK. 