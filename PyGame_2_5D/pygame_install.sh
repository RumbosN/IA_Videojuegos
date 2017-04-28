sudo apt-get update
sudo apt-get install -y python3 mercurial python-dev python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy python3-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
cd ~
hg clone https://bitbucket.org/pygame/pygame
cd pygame
echo "Building pygame"
python3 setup.py build
echo "Installing pygame"
sudo python3 setup.py install
echo "Now try and type in"
echo "import pygame"
echo "and if no error occures, your installation was success"
python3
