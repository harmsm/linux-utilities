#!/usr/bin/env python
__description__ = \
"""
checkFileSize.py

Recursively looks for files greater than some cutoff in a directory.  Useful
when copying to (say) a FAT32 filesystem that cannot take a file > 4 gb.
"""
__author__ = "Michael J. Harms"
__usage__ = "checkFileSize.py directory cutoff_in_gigabytes"
__date__ = "081210"

import os, sys

def main():
    """
    Main function for module.
    """

    try:
        input_dir = sys.argv[1]
        cutoff = float(sys.argv[2])*1e9
    except (IndexError,ValueError):
        print __usage__
        sys.exit()

    for root, dirs, files in os.walk(input_dir):
    
        for f in files:
            size = os.path.getsize(os.path.join(root,f))
            if size > cutoff:
                print "%s: %.3f gb" % (os.path.join(root,f),size/1e9)


if __name__ == "__main__":
    main()
