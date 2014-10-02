
sudo apt-get install pkg-config python-setuptools python-pygame python-opengl python-gst0.10 python-enchant gstreamer0.10-plugins-good python-dev build-essential libgl1-mesa-dev cython libgles2-mesa-dev-lts-saucy

# buggy in 14.04
#sudo apt-get install python-pip

wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
sudo python get-pip.py

sudo easy_install kivy
sudo pip install bintrees

#
sudo pip install guppy
sudo pip install networkx
