from PIL import Image
import os, sys

path = "./"
dirs = os.listdir( path )

for item in dirs:
    if os.path.isfile(path+item):
        if item != 'resize.py':
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((200,200), Image.ANTIALIAS)
            print('saving image: '+item)
            imResize.save(f + '.gif', 'GIF', quality=90)
