'''
Swap the channel of green and alpha for images exported from mali graphics debugger with texture format as rgba4444
Usage:
    python swapPngChannels.py
'''

import os
from PIL import Image

if __name__ == "__main__":
    curDir = os.path.dirname(os.path.realpath(__file__))

    processFiles = []
    for (dirname, dirs, files) in os.walk(curDir):
       for filename in files:
            if filename.endswith('_ga.png'):
                processFiles.append(filename)

    for pngFile in processFiles:
        print("Opening:"+pngFile)
        thefile = os.path.join(curDir, pngFile)
        im = Image.open(thefile)
        #im.load()

        width, height = im.size

        im_rgb = im.convert('RGBA')

        for x in range(0, width):
            for y in range(0,height):
                r, g, b, a = im_rgb.getpixel((x, y))
                im_rgb.putpixel((x, y), (r, a, b, g))

        #outfile, ext = os.path.splitext(infile)
        prefixName = pngFile[:-7]
        outfile = os.path.join(curDir, prefixName + u".png")
        im_rgb.save(outfile, "PNG")

    print("Ding!")