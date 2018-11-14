from PIL import Image
import os
from glob import glob
import help

if __name__ == '__main__':
    size = (600, 400)
    pathList = help.get_filename('E:\\D')
    for path in pathList:
        picName = path.split('\\')[-1]
        img = Image.open(path)
        img.thumbnail(size, Image.ANTIALIAS)
        img.save('E:\\DD\\' + picName)
    print(pathList)