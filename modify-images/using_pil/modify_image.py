#!/usr/bin/env python3
#mortiz feb-2021: In debian this script requires: 
#                 apt-get install python3-pip
#                 pip3 install pillow

from PIL import Image

im = Image.open('myimage.jpg')
im.rotate(45).save('myimage_rotates.jpg')
