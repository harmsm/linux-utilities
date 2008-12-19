#!/usr/bin/env python
__description__ = \
"""
png2swf.py

Program that strings together a set of png files into a flash animation using
python interface to the ming library (http://www.libming.org/).
"""
__author__ = "Michael J. Harms"
__date__ = "080426"
__usage__ = "png2swf.py dir_with_png output_swf"

import os, sys

try:
    import Image
except ImportError:
    print "Python Imaging Library is required to use this script!"
    print "(http://www.pythonware.com/products/pil/)"
    sys.exit()

try:
    from ming import *
except ImportError:
    print "ming flash library python interface is required to use this script!"
    print "(http://www.libming.org/)"
    sys.exit()

def createSwf(png_files,output_file,frame_rate=10):
    """
    Take a list of png files and convert into sequential flash animation.
    """

    # Find the dimensions of the png files.  This is used to determine flash
    # movie dimensions.
    dimensions = dict([(Image.open(p).size,0) for p in png_files])
    dimensions = dimensions.keys()
    if len(dimensions) > 1:
        print "Warning: not all specified png files have the same dimensions!"
    x = min([d[0] for d in dimensions])
    y = min([d[1] for d in dimensions])
 
    # Load png files as ming objects
    frames = [SWFBitmap(p) for p in png_files]

    # Create new swf movie
    m = SWFMovie()
    m.setDimension(x,y)
    m.setBackground(255,255,255)
    m.setRate(float(frame_rate))
    m.setNumberOfFrames(len(frames))

    # Load frames into movie 
    for f in frames:
        m.add(f)
        m.nextFrame()

    # Write output file
    m.save(output_file)

def main():
    """
    Function that parses command line, etc.
    """

    try:
        dir_with_png = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        print __usage__
        sys.exit()
    
    if not os.path.isdir(dir_with_png):
        print "%s is not a directory!" % dir_with_png
        sys.exit()

    # Extract sorted list of .png files in dir_with_png
    png_files = [os.path.join(dir_with_png,p) for p in os.listdir(dir_with_png)]
    png_files = [p for p in png_files if p[-4:] == ".png"]
    png_files.sort()
    if len(png_files) == 0:
        print "%s does not contain any png files!" % dir_with_png
        sys.exit()

    createSwf(png_files,output_file) 


if __name__ == "__main__":
    main()
