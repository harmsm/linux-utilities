#!/usr/bin/env python
"""
split_dir.py

Takes a directory and splits it into some number of smaller directories.
"""

__usage__ = "split_dir.py dir_to_split num_to_split_into"
__author__ = "Michael J. Harms"
__date__ = "070622"

import sys, os, shutil

def splitDir(dir,split):
    """
    Split "dir" into "split" new directories.
    """

    # Contents of dir
    dir_list = os.listdir(dir)
    dir_list.sort()
    
    # Split interval
    l = len(dir_list)
    interval = l/split
    
    # Split dir
    for i in range(split - 1):
        new_dir = "%s_%i" % (dir,i)
        os.mkdir(new_dir)
        file_list = dir_list[i*interval:(i+1)*interval]
        for f in file_list:
            shutil.copy(os.path.join(dir,f),new_dir)

    # Grab last part of directory (even if not divisible by split)
    new_dir = "%s_%i" % (dir,i+1)
    os.mkdir(new_dir)
    file_list = dir_list[(i+1)*interval:]
    for f in file_list:
        shutil.copy(os.path.join(dir,f),new_dir)


def main():
    """
    To be called if user runs program from command line.
    """

    try:
        dir = sys.argv[1].strip(os.sep)
        split = int(sys.argv[2])
    except IndexError:
        print __usage__
        sys.exit()

    if os.path.isdir(dir):
        splitDir(dir,split)
    else:
        err = "%s is not a directory" % dir
        raise IOError(err)

# If called from the command line
if __name__ == "__main__":
    main()

