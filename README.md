<div align="center">

![icon](data/icons/com.github.hezral.quickword.svg)

# ![logo_type](data/logo_type.png?raw=true)
</div>

If you like what i make, it would really be nice to have someone buy me a coffee

<a href="https://www.buymeacoffee.com/hezral" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

### Quickly lookup words on the fly and offline
* On the fly word lookup
* Works offline (first run will require internet to download dictionary data)
* Copy definitions and examples to clipboard with just a click
* Word definitions
* Examples of word sentences
* Synonyms
* Explore synonyms from each word

| ![Screenshot](data/screenshot-01.png?raw=true) | ![Screenshot](data/screenshot-02.png?raw=true) | ![Screenshot](data/screenshot-03.png?raw=true) |
|------------------------------------------|-----------------------------------------|-----------------------------------------|

## Demo and How to use
QuickWord can be used by manual lookup and via a keyboard shortcut to open it on the fly. 

Select a word and hit the a keyboard shortcut to get the lookup. Recommended shortcut: ⌘ + D
* Manual entry of words
* Selecting a text

![](data/demo.gif)

# Installation
QuickWord is availble for installation in the following Linux Distributions
<a href="https://repology.org/project/quickword/versions">
    <img src="https://repology.org/badge/vertical-allrepos/quickword.svg" alt="Packaging status" align="right">
</a>


## Build using flatpak
* requires that you have flatpak-builder installed
* flatpak enabled
* flathub remote enabled

```
flatpak-builder --user --force-clean --install build-dir com.github.hezral.quickword.yml
```

### Build using meson 
Ensure you have these dependencies installed

* python3
* python3-gi
* libgranite-dev
* python-xlib
* xclip
* pynput

Download the updated source [here](https://github.com/hezral/quickword/archive/master.zip), or use git:
```bash
git clone https://github.com/hezral/quickword.git
cd clips
meson build --prefix=/usr
cd build
ninja build
sudo ninja install
```
The desktop launcher should show up on the application launcher for your desktop environment
if it doesn't, try running
```
com.github.hezral.quickword
```

## Thanks/Credits
- [Wordnet](http://wordnetweb.princeton.edu/perl/webwn) Definitions are based on Wordnet.
- [Ideogram](https://appcenter.elementary.io/com.github.cassidyjames.ideogram/) Inspired by it. Also borrowed/forked some code.
- [ElementaryPython](https://github.com/mirkobrombin/ElementaryPython) This started me off on coding with Python and GTK. 
