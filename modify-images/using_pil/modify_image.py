#!/usr/bin/env python3
#mortiz feb-2021: In debian this script requires: 
#                 apt-get install python3-pip
#                 pip3 install pillow

from PIL import Image
import os, os.path


imgPath='/home/student-01-5c85541b1d5e/images/'
imgSavePath='/opt/icons/'

print ('Original Images')
for f in os.listdir(imgPath):
    if not f.startswith('.'):
        img = Image.open(imgPath + f)
        print(img.format, img.size)
        img = img.convert('RGB')
        img = img.resize((128, 128))
        img.rotate(90).save(imgSavePath + f + '.jpeg')

print ('Fixed Images')
for f in os.listdir(imgSavePath):
    img = Image.open(imgSavePath + f)
    print(img.format, img.size)

